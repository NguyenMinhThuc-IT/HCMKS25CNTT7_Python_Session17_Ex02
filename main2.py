product_list = [
    "P01-Tai Nghe Bluetooth-550000-4.5",
    "P02-Chuột Không Dây-250000-4.8",
    "P03-Bàn Phím Cơ-850000-4.5"
]

def get_validate_input(prompt, input_type):
    while True:
        user_input = input(prompt).strip()
        if not user_input:
            print("Lỗi: Dữ liệu nhập vào không được để trống!")
            continue
        try:
            return input_type(user_input)
        except ValueError:
            if input_type == int:
                print("Lỗi: Vui lòng nhập một số nguyên hợp lệ!")
            else:
                print("Lỗi: Định dạng dữ liệu không hợp lệ!")

def display_labels(products):
    print("\n--- DANH SÁCH TEM NHÃN ---")
    template = "Mã: {id:<10} | Tên: {name:<25} | Giá: {price_formatted} VND | Rating: {rating}*"
    
    for item in products:
        parts = item.split('-')
        
        if len(parts) < 4:
            try:
                invalid_id = parts[0] if len(parts) > 0 else "Unknown"
                print(f"[ERR] Bỏ qua sản phẩm [{invalid_id}] do sai cấu trúc dữ liệu (Thiếu trường).")
            except IndexError:
                print("[ERR] Bỏ qua một sản phẩm lỗi cấu trúc nghiêm trọng.")
            continue
            
        p_id, name, raw_price, raw_rating = parts[0], parts[1], parts[2], parts[3]
        
        if not raw_price.isdigit():
            print(f"[ERR] Bỏ qua sản phẩm [{p_id}] do lỗi định dạng giá tiền (Chứa ký tự lạ).")
            continue
            
        try:
            price = int(raw_price)
            rating = float(raw_rating)
        except ValueError:
            print(f"[ERR] Bỏ qua sản phẩm [{p_id}] do lỗi ép kiểu dữ liệu số học.")
            continue
            
        data_map = {
            "id": p_id,
            "name": name,
            "price_formatted": f"{price:,}",
            "rating": rating
        }
        
        print(template.format_map(data_map))

def sort_products_smart(products):
    print("\n--- SẮP XẾP SẢN PHẨM ---")
    
    def extract_sort_key(item):
        parts = item.split('-')
        if len(parts) < 4:
            return (0.0, 0)
        
        raw_price = parts[2]
        raw_rating = parts[3]
        
        cleaned_price = "".join([char for char in raw_price if char.isdigit()])
        
        try:
            rating = float(raw_rating)
            price = int(cleaned_price) if cleaned_price else 0
            return (-rating, price)
        except ValueError:
            return (0.0, 0)

    products.sort(key=extract_sort_key)
    print("Đã sắp xếp thành công! Cập nhật danh sách:")
    for i in range(len(products)):
        print(f"{i + 1}. {products[i]}")

def calculate_total_inventory_value(products):
    print("\n--- TỔNG GIÁ TRỊ KHO ---")
    valid_prices = []
    
    for item in products:
        parts = item.split('-')
        if len(parts) >= 3:
            raw_price = parts[2]
            cleaned_price = "".join([char for char in raw_price if char.isdigit()])
            if cleaned_price:
                valid_prices.append(int(cleaned_price))
                
    if len(valid_prices) == 0:
        print("Tổng giá trị các mặt hàng hiện tại là: 0 VND.")
        return 0
        
    total_value = 0
    for price in valid_prices:
        total_value += price
        
    print(f"Tổng giá trị các mặt hàng hiện tại là: {total_value:,} VND.")
    return total_value

def main():
    while True:
        print("\n============= E-COMMERCE ANALYTICS =============")
        print("1. Hiển thị tem nhãn sản phẩm (format_map & F-String)")
        print("2. Sắp xếp sản phẩm thông minh (sort key)")
        print("3. Tính tổng giá trị kho hàng (vòng lặp tích lũy)")
        print("4. Đóng hệ thống")
        print("================================================")
        
        choice = get_validate_input("Chọn chức năng (1-4): ", int)
        
        if choice == 1:
            display_labels(product_list)
        elif choice == 2:
            sort_products_smart(product_list)
        elif choice == 3:
            calculate_total_inventory_value(product_list)
        elif choice == 4:
            print("Đang đóng hệ thống phân tích. Hẹn gặp lại!")
            break
        else:
            print("Lựa chọn không hợp lệ! Vui lòng chọn một số trong phạm vi từ 1 đến 4.")

if __name__ == "__main__":
    main()