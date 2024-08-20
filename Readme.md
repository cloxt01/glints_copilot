### Konfigurasi Playwright untuk Glints API

## Struktur File

## `cookie.json`

File `cookie.json` menyimpan cookie untuk autentikasi ke dalam server API Glints:

**Example**
```json
{
	"Kuki permintaan": {
		"name" : "value"
	}
}
```

## `config.json`

File `config.json` menyimpan konfigurasi yang diperlukan untuk skrip. Berikut adalah struktur dan nilai-nilai yang tersedia:

**type**: Jenis pekerjaan yang dicari.
- **Opsi**: `"FULL_TIME"`, `"CONTRACT"`, `"INTERNSHIP"`, `"PART_TIME"`, `"DAILY"`, `"PROJECT_BASED"`

**workArrangementOptions**: Opsi pengaturan kerja.
- **Opsi**: `"REMOTE"`, `"HYBRID"`, `"ONSITE"`

**sortBy**: Metode pengurutan hasil pencarian.
- **Opsi**: `"LATEST"`, `"RELEVANCE"`

**lastUpdatedAtRange**: Rentang waktu pembaruan pekerjaan.
- **Opsi**: `"PAST_24_HOURS"`, `"PAST_WEEK"`, `"PAST_MONTH"`, `"ANY_TIME"`

**range**: Rentang pengalaman yang dicari.
- **Opsi**: `"FRESH_GRAD"`, `"NO_EXPERIENCE"`, `"LESS_THAN_A_YEAR"`, `"ONE_TO_THREE_YEARS"`, `"THREE_TO_FIVE_YEARS"`, `"FIVE_TO_TEN_YEARS"`, `"MORE_THAN_TEN_YEARS"`

**educationLevels**: Tingkat pendidikan yang diinginkan.
- **Opsi**: `"HIGH_SCHOOL"`, `"DIPLOMA"`, `"SECONDARY_SCHOOL"`, `"PRIMARY_SCHOOL"`, `"BACHELOR_DEGREE"`, `"MASTER_DEGREE"`, `"DOCTORATE"`

**includeExternalJobs**: Sertakan pekerjaan dari luar.
- **Opsi**: `true`, `false`

## Cara Menggunakan

1. **Instalasi**: Pastikan Playwright dan dependensi terkait terinstal.
2. **Konfigurasi**: Sesuaikan nilai dalam file `config.json` sesuai kebutuhan Anda.
3. **Jalankan Skrip**: Eksekusi skrip Python untuk memulai pencarian pekerjaan dan aplikasi.

## Penting

- **Periksa Format Cookies dan Konfigurasi: Pastikan format data dalam cookie.json dan config.json sesuai dengan yang diharapkan. Kesalahan dalam penulisan atau nilai yang tidak valid dapat menyebabkan kegagalan dalam permintaan API atau hasil yang tidak diinginkan.**
- **Perbarui Token jika Diperlukan: Jika API memerlukan token atau header khusus, pastikan untuk memperbarui skrip dengan informasi yang relevan.**

**!** **Kesalahan dalam penulisan opsi dapat menyebabkan kesalahan dalam permintaan API dan hasil yang tidak diinginkan** **!**