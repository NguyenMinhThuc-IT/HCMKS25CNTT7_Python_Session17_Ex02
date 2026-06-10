product_list = [
    "P01-Tai Nghe Bluetooth-550000-4.5",
    "P02-Chuột Không Dây-250000-4.8",
    "P03-Bàn Phím Cơ-850000-4.5"
]

def get_validate_input(prompt: str, input_type) -> any:
    """Yêu cầu người dùng nhập dữ liệu từ bàn phím, kiểm tra bẫy rỗng 
    và ép kiểu dữ liệu an toàn theo yêu cầu.

    Args:
        prompt (str): Câu lệnh hướng dẫn hiển thị ra màn hình cho người dùng.
        input_type (type): Kiểu dữ liệu mong muốn ép sang (Ví dụ: int, float, str).

    Returns:
        any: Giá trị nhập hợp lệ đã được ép sang kiểu dữ liệu mong muốn.
    """
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

def display_labels(products: list) -> None:
    """Trích xuất, xử lý chuỗi phẳng của từng sản phẩm và hiển thị 
    dưới dạng tem nhãn căn lề chuẩn hóa thông qua phương thức format_map.

    Args:
        products (list): Danh sách các chuỗi dữ liệu sản phẩm gốc.
    """
    print("\n-------------------------------------------------")
    print("--- 1. HIỂN THỊ TEM NHÃN SẢN PHẨM ---")
    print("-------------------------------------------------")
    
    template = "Mã: {id:<10} | Tên: {name:<25} | Giá: {price_formatted} VND | Rating: {rating}*"
    
    for item in products:
        parts = item.split('-')
        
        # Kiểm tra bẫy thiếu trường thông tin dữ liệu
        if len(parts) < 4:
            try:
                invalid_id = parts[0] if len(parts) > 0 else "Unknown"
                print(f"[ERR] Bỏ qua sản phẩm [{invalid_id}] do sai cấu trúc dữ liệu (Thiếu trường).")
            except IndexError:
                print("[ERR] Bỏ qua một sản phẩm lỗi cấu trúc nghiêm trọng.")
            continue
            
        p_id, name, raw_price, raw_rating = parts[0], parts[1], parts[2], parts[3]
        
        # Kiểm tra bẫy dữ liệu giá tiền chứa ký tự lạ
        if not raw_price.isdigit():
            print(f"[ERR] Bỏ qua sản phẩm [{p_id}] do lỗi định dạng giá tiền (Chứa ký tự lạ).")
            continue
            
        try:
            price = int(raw_price)
            rating = float(raw_rating)
        except ValueError:
            print(f"[ERR] Bỏ qua sản phẩm [{p_id}] do lỗi ép kiểu dữ liệu số học.")
            continue
            
        # Áp dụng cơ chế ánh xạ dữ liệu trực tiếp qua format_map
        data_map = {
            "id": p_id,
            "name": name,
            "price_formatted": f"{price:,}",
            "rating": rating
        }
        
        print(template.format_map(data_map))


def sort_products_smart(products: list) -> None:
    """Sắp xếp danh sách sản phẩm theo cơ chế đa tiêu chí bằng Custom Sort Key:
    Ưu tiên Rating cao nhất xếp trước (giảm dần), nếu trùng Rating thì 
    xếp theo Giá tiền thấp nhất (tăng dần).

    Args:
        products (list): Danh sách các chuỗi dữ liệu sản phẩm cần sắp xếp.
    """
    print("\n-------------------------------------------------")
    print("--- 2. SẮP XẾP SẢN PHẨM THÔNG MINH ---")
    print("-------------------------------------------------")
    
    def extract_sort_key(item):
        """Hàm nội bộ bóc tách chuỗi tạo khóa Tuple phục vụ thuật toán sắp xếp."""
        parts = item.split('-')
        if len(parts) < 4:
            return (0.0, 0)
        
        raw_price = parts[2]
        raw_rating = parts[3]
        
        # Làm sạch chuỗi giá, chỉ giữ lại các ký tự là số số học
        cleaned_price = "".join([char for char in raw_price if char.isdigit()])
        
        try:
            rating = float(raw_rating)
            price = int(cleaned_price) if cleaned_price else 0
            # 💡 Kỹ thuật phản đảo dấu (-rating) giúp đảo chiều sắp xếp giảm dần cho Rating
            return (-rating, price)
        except ValueError:
            return (0.0, 0)

    # Thực hiện sắp xếp tại chỗ (In-place sorting)
    products.sort(key=extract_sort_key)
    print("=> THÀNH CÔNG: Đã cập nhật thứ tự danh sách kho hàng:")
    for i in range(len(products)):
        print(f"  {i + 1}. {products[i]}")


def calculate_total_inventory_value(products: list) -> int:
    """Bóc tách dữ liệu giá, thực hiện xử lý loại bỏ ký tự rác và 
    tính tổng giá trị tích lũy của toàn bộ kho hàng.

    Args:
        products (list): Danh sách các chuỗi dữ liệu sản phẩm trong kho.

    Returns:
        int: Tổng giá trị tiền mặt tích lũy của kho hàng (VND).
    """
    print("\n-------------------------------------------------")
    print("--- 3. TÍNH TỔNG GIÁ TRỊ KHO HÀNG ---")
    print("-------------------------------------------------")
    
    valid_prices = []
    
    for item in products:
        parts = item.split('-')
        if len(parts) >= 3:
            raw_price = parts[2]
            cleaned_price = "".join([char for char in raw_price if char.isdigit()])
            if cleaned_price:
                valid_prices.append(int(cleaned_price))
                
    if len(valid_prices) == 0:
        print("=> Kết quả: Tổng giá trị các mặt hàng hiện tại là: 0 VND.")
        return 0
        
    # Vòng lặp tích lũy giá trị tổng thể
    total_value = 0
    for price in valid_prices:
        total_value += price
        
    print(f"=> Kết quả: Tổng giá trị các mặt hàng hiện tại là: {total_value:,} VND.")
    return total_value


def display_menu() -> None:
    """Hiển thị giao diện menu chức năng điều khiển dạng Console trực quan."""
    show_menu = """
============= E-COMMERCE ANALYTICS =============
1. Hiển thị tem nhãn sản phẩm (format_map & F-String)
2. Sắp xếp sản phẩm thông minh (sort key)
3. Tính tổng giá trị kho hàng (vòng lặp tích lũy)
4. Đóng hệ thống
================================================"""
    print(show_menu)

def main() -> None:
    """Hàm khởi chạy trung tâm, quản lý luồng chọn chức năng của hệ thống."""
    while True:
        display_menu()
        choice = get_validate_input("Chọn chức năng (1-4): ", int)
        
        if choice == 1:
            display_labels(product_list)
        elif choice == 2:
            sort_products_smart(product_list)
        elif choice == 3:
            calculate_total_inventory_value(product_list)
        elif choice == 4:
            print("\n[HỆ THỐNG] Đang đóng hệ thống phân tích.")
            print("=> Trạng thái: Kết thúc ca làm việc an toàn. Hẹn gặp lại!")
            break
        else:
            print("\nLỗi: Lựa chọn không hợp lệ! Vui lòng chọn số trong phạm vi từ 1 đến 4.")


if __name__ == "__main__":
    main()