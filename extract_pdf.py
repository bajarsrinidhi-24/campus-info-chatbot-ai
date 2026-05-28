from pypdf import PdfReader

reader = PdfReader(r"C:\Users\HP\Downloads\CSE.pdf")
text = ""
for page in reader.pages:
    text += page.extract_text()

print(f"Extracted {len(text)} characters")

# Save to file
with open("syllabus/cse_syllabus.txt", "w", encoding="utf-8") as f:
    f.write(text)

print("Saved to syllabus/cse_syllabus.txt")