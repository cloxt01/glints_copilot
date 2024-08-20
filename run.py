import json
from playwright.sync_api import sync_playwright

def main():
    # Membaca cookies dari file JSON dengan encoding UTF-8
    with open('cookie.json', 'r', encoding='utf-8') as file:
        cookies_data = json.load(file)
    
    cookies = cookies_data["Kuki permintaan"]

    # Membaca konfigurasi dari file JSON dengan encoding UTF-8
    with open('config.json', 'r', encoding='utf-8') as file:
        config_data = json.load(file)
    
    graphql_variables = config_data["graphql_variables"]
    application_payload = config_data["application_payload"]

    # Memulai Playwright dan membuka browser dengan context yang sudah diatur
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Ganti dengan p.firefox jika menggunakan Firefox
        context = browser.new_context()
        
        # Menambahkan cookies ke context
        context.add_cookies([
            {
                'name': name,
                'value': value,
                'domain': '.glints.com',
                'path': '/',
                'sameSite': 'Lax',
            }
            for name, value in cookies.items()
        ])

        # Membuka halaman dan mengambil jobs_id (jika perlu)
        page = context.new_page()
        page.goto('https://glints.com/')

        # Payload untuk permintaan GraphQL
        graphql_payload = {
            "operationName": "searchJobs",
            "variables": graphql_variables,
            "query": """
                query searchJobs($data: JobSearchConditionInput!) {
                  searchJobs(data: $data) {
                    jobsInPage {
                      id
                      title
                      workArrangementOption
                      status
                      createdAt
                      updatedAt
                      isActivelyHiring
                      isHot
                      isApplied
                      shouldShowSalary
                      educationLevel
                      type
                      fraudReportFlag
                      salaryEstimate {
                        minAmount
                        maxAmount
                        CurrencyCode
                        __typename
                      }
                      company {
                        ...CompanyFields
                        __typename
                      }
                      citySubDivision {
                        id
                        name
                        __typename
                      }
                      city {
                        ...CityFields
                        __typename
                      }
                      country {
                        ...CountryFields
                        __typename
                      }
                      salaries {
                        ...SalaryFields
                        __typename
                      }
                      location {
                        ...LocationFields
                        __typename
                      }
                      minYearsOfExperience
                      maxYearsOfExperience
                      source
                      type
                      hierarchicalJobCategory {
                        id
                        level
                        name
                        children {
                          name
                          level
                          id
                          __typename
                        }
                        parents {
                          id
                          level
                          name
                          __typename
                        }
                        __typename
                      }
                      skills {
                        skill {
                          id
                          name
                          __typename
                        }
                        mustHave
                        __typename
                      }
                      traceInfo
                      __typename
                    }
                    numberOfJobsCreatedInLast14Days
                    totalJobs
                    expInfo
                    __typename
                  }
                }
                
                fragment CompanyFields on Company {
                  id
                  name
                  logo
                  status
                  isVIP
                  IndustryId
                  industry {
                    id
                    name
                    __typename
                  }
                  __typename
                }
                
                fragment CityFields on City {
                  id
                  name
                  __typename
                }
                
                fragment CountryFields on Country {
                  code
                  name
                  __typename
                }
                
                fragment SalaryFields on JobSalary {
                  id
                  salaryType
                  salaryMode
                  maxAmount
                  minAmount
                  CurrencyCode
                  __typename
                }
                
                fragment LocationFields on HierarchicalLocation {
                  id
                  name
                  administrativeLevelName
                  formattedName
                  level
                  slug
                  parents {
                    id
                    name
                    administrativeLevelName
                    formattedName
                    level
                    slug
                    parents {
                      level
                      formattedName
                      slug
                      __typename
                    }
                    __typename
                  }
                  __typename
                }
            """
        }
        
        # Mengirim permintaan GraphQL
        response = page.evaluate(f"""
            async () => {{
                const response = await fetch('https://glints.com/api/v2/graphql?op=searchJobs', {{
                    method: 'POST',
                    headers: {{
                        'Content-Type': 'application/json',
                    }},
                    body: JSON.stringify({json.dumps(graphql_payload)})
                }});
                return await response.json();
            }}
        """)

        # Memeriksa apakah response valid
        if 'data' not in response or 'searchJobs' not in response['data']:
            print("Error: Invalid response from GraphQL API.")
            return

        jobs = response['data']['searchJobs']['jobsInPage']

        # Mendapatkan ID dari setiap pekerjaan
        job_ids = [job['id'] for job in jobs]
        companies = [job['company']['name'] for job in jobs]

        # Mengirim permintaan POST untuk setiap job ID
        for job_id, company_name in zip(job_ids, companies):
            response = page.evaluate(f"""
                async () => {{
                    const response = await fetch('https://glints.com/api/v2-alc/v2/jobs/{job_id}/applications', {{
                        method: 'POST',
                        headers: {{
                            'Content-Type': 'application/json',
                        }},
                        body: JSON.stringify({json.dumps(application_payload)})
                    }});
                    return await response.json();
                }}
            """)
            
            # Menampilkan hasil
            if 'error' in response:
                if "already exists" in response['error']['details'][0].lower():
                    print(f"already | {company_name} | {job_id}")
                else:
                    print(f"Job ID {job_id}: Error occurred - {response['error']['details']}")
            elif 'data' in response and response['data']['status'] == 'NEW':
                print(f"success | {company_name} | {job_id}")
            else:
                print("An error occurred | line 247")
        
        browser.close()

if __name__ == "__main__":
    main()
