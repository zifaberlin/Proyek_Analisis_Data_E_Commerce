 Proyek Analisis Data E-Commerce

 Deskripsi Proyek
Proyek ini bertujuan untuk menganalisis **E-Commerce Public Dataset** guna mengetahui pengaruh keterlambatan pengiriman terhadap kepuasan pelanggan, metode pembayaran yang paling dominan, serta segmentasi pelanggan berdasarkan analisis RFM.

 Pertanyaan Bisnis
1. Apakah terdapat perbedaan signifikan pada rata-rata review score antara pesanan yang dikirim tepat waktu dan pesanan yang terlambat selama periode September 2016 hingga Agustus 2018?

2. Metode pembayaran apa yang paling banyak digunakan dan menghasilkan total transaksi terbesar selama periode September 2016 hingga Agustus 2018?
3. Bagaimana distribusi pelanggan ke dalam segmen berdasarkan analisis RFM?

Insight Utama

- Pesanan yang dikirim tepat waktu memiliki rata-rata review score lebih tinggi dibandingkan pesanan yang terlambat.
- Keterlambatan pengiriman berpengaruh terhadap tingkat kepuasan pelanggan.
- Metode pembayaran tertentu mendominasi jumlah transaksi dan kontribusi revenue.
- Sebagian besar pelanggan berada pada segmen **Regular Customer**.
- Terdapat pelanggan bernilai tinggi pada segmen **Best Customer** yang perlu dipertahankan.
- Segmen **Lost Customer** menunjukkan pelanggan yang perlu diaktivasi kembali.


 Struktur Folder

- `Proyek_Analisis_Data.ipynb`
- `dashboard.py`
- `requirements.txt`
- `README.md`
- `orders_dataset.csv`
- `order_reviews_dataset.csv`
- `order_payments_dataset.csv`

  Setup Environment

````markdown
## Setup Environment

1. Buat virtual environment:
```bash
python -m venv venv
````

2. Aktifkan virtual environment:

Windows:

```bash
venv\Scripts\activate
```

Mac/Linux:

```bash
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Menjalankan Dashboard

```bash
streamlit run dashboard.py
```





