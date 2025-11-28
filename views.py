rom django.shortcuts import render
from django.http import HttpResponse

# 📚 Kitoblar ro‘yxati
books = [
    {"id": 1, "title": "Alpomish", "description": "„Alpomish“ — oʻzbek xalq ogʻzaki badiiy ijodidagi qahramon personaj. Turkiy xalqlarda ogʻizdan ogʻizga oʻtib kelayotgan biylarning sardori."},
    {"id": 2, "title": "Sariq devni minib", "description": "„Sariq devni minib“ romani (1968) yozuvchiga katta shuhrat keltirgan. Yozuvchi Xudoyberdi To'xtaboyev"},
    {"id": 3, "title": "Dunyo ishlari", "description": "„Dunyoning ishlari“ — Oʻzbekiston xalq yozuvchisi Oʻtkir Hoshimov qalamiga mansub memuar qissa. Asar katta-kichik hikoyalardan iborat, uzoq yillar davomida yozilgan va toʻliq tarzda 2005-yilda Sharq nashriyoti tomonidan nashr etilgan. Keyinchalik boshqa nashriyotlar tomonidan ham koʻp bora qayta nashr etildi."}
]

def book_list(request):
    html = "<h1>📚 Kitoblar ro‘yxati</h1><ul>"
    for book in books:
        html += f'<li><a href="/book/{book["id"]}/">{book["title"]}</a></li>'
    html += "</ul>"
    return HttpResponse(html)

def book_detail(request, book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if not book:
        return HttpResponse("<h2>Kitob topilmadi</h2>")
    html = f"<h2>{book['title']}</h2><p>{book['description']}</p>"
    html += '<a href="/">🔙 Ortga</a>'
    return HttpResponse(html)
