import os
from src.smg_llie import SMG_LLIE_Enhancer

def main():
    print("\n=== SMG-LLIE SYSTEM START ===")

    # Inisialisasi model
    enhancer = SMG_LLIE_Enhancer()

    input_folder = "data/input"

    # Validasi folder input
    if not os.path.exists(input_folder):
        print("❌ Folder input tidak ditemukan!")
        return

    files = os.listdir(input_folder)

    if not files:
        print("❌ Folder input kosong!")
        return

    print(f"\n📂 Total file ditemukan: {len(files)}")

    processed = 0

    for filename in files:
        if filename.lower().endswith((".jpg", ".png", ".jpeg")):

            image_path = os.path.join(input_folder, filename)

            print(f"\n[PROCESSING] {filename}")

            try:
                enhancer.enhance(image_path, visualize=False)
                processed += 1

            except Exception as e:
                print(f"❌ Error pada {filename}: {e}")

    print("\n=== SELESAI ===")
    print(f"✅ Total berhasil diproses: {processed}")

if __name__ == "__main__":
    main()