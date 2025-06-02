from fastapi import FastAPI
from fastapi.responses import FileResponse
from PIL import Image
import requests
from io import BytesIO

app = FastAPI()

# ฟังก์ชันโหลดภาพจาก URL
def load_image_from_url(url):
    response = requests.get(url)
    response.raise_for_status()
    return Image.open(BytesIO(response.content)).convert("RGBA")

@app.get("/")
def read_root():
    return {"message": "✅ Image merge API is running"}

@app.post("/merge")
def merge_images():
    # URLs
    cover_url = "https://pub-a596a6a5511b481cb3740594776a7747.r2.dev/PGZEEDAUTO%20COVER.png"
    main_url = "https://oaidalleapiprodscus.blob.core.windows.net/private/org-NRB6PfiDynQuB1og3W4Gfz5n/user-yFgbWYdM6RNDf9lat9ysGn6s/img-2sZuraf4xbMS8416F3YEz5Jz.png?st=2025-06-02T13%3A12%3A50Z&se=2025-06-02T15%3A12%3A50Z&sp=r&sv=2024-08-04&sr=b&rscd=inline&rsct=image/png&skoid=cc612491-d948-4d2e-9821-2683df3719f5&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-06-02T04%3A06%3A19Z&ske=2025-06-03T04%3A06%3A19Z&sks=b&skv=2024-08-04&sig=boxVZadlwqFY4rSy2Ih9cq%2Bg0xqaLHvH0XhpirI/qrA%3D"
    logo_url = "https://pgzeedauto.games/wp-content/uploads/elementor/thumbs/cropped-pgzeedauto-logo-1-qrv2jpriuez7sj7kzrhgmhn6je94zppamhjucngrog.webp"

    # โหลดภาพ
    cover = load_image_from_url(cover_url)
    main = load_image_from_url(main_url)
    logo = load_image_from_url(logo_url)

    # ปรับขนาด main ให้พอดีกับ cover
    main_resized = main.resize((cover.width, int(main.height * (cover.width / main.width))))
    cover.paste(main_resized, (0, 0), main_resized)

    # ปรับขนาด logo แล้ววางมุมขวาบน
    logo_resized = logo.resize((200, 200))
    logo_position = (cover.width - 200 - 15, 15)
    cover.paste(logo_resized, logo_position, logo_resized)

    # บันทึกไฟล์ผลลัพธ์
    output_path = "final_combined_image.png"
    cover.save(output_path)

    # ส่งไฟล์กลับ
    return FileResponse(output_path, media_type="image/png", filename="merged.png")
