import fitz

def extract_images(path: str):
    # Open the PDF
    pdf_file = fitz.open(path)

    # Iterate through each page
    for page_index in range(len(pdf_file)):
        page = pdf_file[page_index]
        image_list = page.get_images()
        
        # Print the number of images on this page
        if image_list:
            print(f"[+] Found a total of {len(image_list)} images on page {page_index}")
        else:
            print(f"[!] No images found on page {page_index}")
        
        # Extract each image
        for image_index, img in enumerate(image_list, start=1):
            # img is a tuple: (xref, smask, width, height, bpc, colorspace, alt. colorspace, name, filter, referencer)
            xref = img[0]  # Get just the xref number (first element of tuple)
            
            base_image = pdf_file.extract_image(xref)
            image_bytes = base_image["image"]
            
            # Save the image
            image_ext = base_image["ext"]
            image_name = f"images/image{page_index+1}_{image_index}.{image_ext}"
            
            with open(image_name, "wb") as image_file:
                image_file.write(image_bytes)
                print(f"[+] Saved: {image_name}")

    pdf_file.close()