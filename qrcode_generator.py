import qrcode 

# Your website
url = "https://forla-research.github.io/"

# Generate static QR
img = qrcode .make(url)

# Save as PNG
img.save("forla_qr.png")
