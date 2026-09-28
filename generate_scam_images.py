import os

from PIL import Image, ImageDraw, ImageFont

def create_scam_image(text, filename, bg_color=(236, 229, 221), text_bg=(255, 255, 255)):

    
    img_width, img_height = 800, 600
    image = Image.new('RGB', (img_width, img_height), color=bg_color)
    draw = ImageDraw.Draw(image)
    
    # Try to load a default font, fallback to basic if not found
    try:
        # Windows default font
        font = ImageFont.truetype("arial.ttf", 24)
    except IOError:
        font = ImageFont.load_default()

    # Draw message bubble
    bubble_margin = 40
    bubble_padding = 20
    
    # Rough estimation of text size
    # We will split text into multiple lines if it's too long
    words = text.split(' ')
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + word + " "
        # Get bounding box of the text to check width
        left, top, right, bottom = draw.textbbox((0,0), test_line, font=font)
        if (right - left) > (img_width - 2 * bubble_margin - 2 * bubble_padding):
            lines.append(current_line)
            current_line = word + " "
        else:
            current_line = test_line
    lines.append(current_line)

    # Calculate bubble height
    line_height = bottom - top
    bubble_height = len(lines) * (line_height + 5) + 2 * bubble_padding
    
    # Draw bubble rectangle
    bubble_coords = [
        bubble_margin, 
        bubble_margin, 
        img_width - bubble_margin, 
        bubble_margin + bubble_height
    ]
    draw.rounded_rectangle(bubble_coords, radius=10, fill=text_bg, outline=(200, 200, 200))
    
    # Draw text
    y_text = bubble_margin + bubble_padding
    for line in lines:
        draw.text((bubble_margin + bubble_padding, y_text), line, font=font, fill=(0, 0, 0))
        y_text += line_height + 5

    # Save image
    output_path = os.path.join("test_images", filename)
    image.save(output_path)
    print(f"Created {output_path}")

# Scam 1: Electricity Bill
text1 = "Dear Customer, Your electricity power will be disconnected tonight at 9:30 PM from update office. because your previous month bill was not update. Please immediately contact with our electricity officer 9876543210 Thank You."
create_scam_image(text1, "electricity_scam.png")

# Scam 2: KBC Lottery
text2 = "CONGRATULATIONS!! You have won a lottery of Rs. 25,00,000 from Kaun Banega Crorepati (KBC) & Jio. To claim your prize money, please call the KBC Head Office Manager Mr. Rana Pratap on this WhatsApp number: +91 8888888888. Do not share this message with anyone."
create_scam_image(text2, "kbc_lottery_scam.png")

# Scam 3: Part-time Job
text3 = "Hello, I am a recruiter from Global Tech. We are offering a part-time job that you can do from home using your mobile phone. You just need to like YouTube videos and subscribe to channels. Daily salary is Rs. 3000 to Rs. 5000. If you are interested, please reply YES or click this link: http://bit.ly/fake-job-offer"
create_scam_image(text3, "part_time_job_scam.png")

# Scam 4: Hinglish OTP scam
text4 = "Namaskar, aapka bank account temporarily block kar diya gaya hai KYC pending hone ke karan. Kripya apna account unblock karne ke liye is link par click karein aur apna OTP verify karein: http://sbi-kyc-update-online.com/ jaldi karein varna penalty lagegi."
create_scam_image(text4, "hinglish_kyc_scam.png")
