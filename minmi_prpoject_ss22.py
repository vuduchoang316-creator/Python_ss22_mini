import logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] - [%(levelname)s] - %(message)s",
    encoding='UTF8'
)

devices = [
    {'id': 'M01', 'location': 'Mechanical Shop A', 'old_index': 1200, 'new_index': 4500, 'status': 'Normal'},
    {'id': 'M02', 'location': 'Assembly Line B', 'old_index': 2300, 'new_index': 8500, 'status': 'Overload'}
]

def display_info(devices):
    if not devices:
        print("Hệ thống hiện chưa có thiết bị giám sát nào !")
        return
    print("--- DANH SÁCH THIẾT BỊ GIÁM SÁT ---")
    print(f"{'Mã TB':<10} | {'Vị trí phân xưởng' :<20} | {'Chỉ số Cũ':<10} | {'Chỉ số mới':<10} | {'Trạng thái'}")
    for value in devices:
        print("{id:<10} | {location:<20} | {old_index:<10} | {new_index:<10} | {status}".format_map(value))
    logging.info("Người dùng đã xem sanh sách.")
def check_id(devices,input_id):
    for i , value in enumerate(devices):
        if value['id'] == input_id:
            return i
    return -1

def update_indices(devices):
    input_id = input("Nhập mã thiết bị: ").strip().upper()
    index = check_id(devices,input_id)
    if not input_id:
        print("Mã ID không hợp lệ (Không được để trống)")
        return
    if check_id(devices,input_id) == -1:
        print("Lỗi: (ERR-E01): Mã thiết bị này không tồn tại trong danh sách hệ thống")
        return
    while True:
        try:
            input_old_index = int(input("Nhập chỉ số cũ: "))
            if input_old_index < 0:
                print("[Lỗi] (ERR-E03): Định dạng không hợp lệ! Chỉ số điện phải là số lớn hơn hoặc bằng 0!")
                logging.error("The index must not be negative.")
                continue
        except ValueError:
            print("Chỉ số nhập vào không hợp lệ")
            logging.error(f"Invalid index {input_old_index}")
            continue
        break
    while True:
        try:
            input_new_index = int(input("Nhập chỉ số mới: "))
            if input_new_index < 0:
                print("[Lỗi] (ERR-E03): Định dạng không hợp lệ! Chỉ số điện phải là số lớn hơn hoặc bằng 0!")
                
                continue
            if input_new_index < input_old_index:
                print("[Lỗi](ERR-E02): Chỉ số mới không được nhỏ hơn chỉ số cũ")
                logging.error("The index must not be negative.")
                continue
        except ValueError:
            print("Lỗi chỉ số không hợp lệ")
            logging.error(f"Invalid index {input_new_index}")
            continue
        break
    devices[index]['old_index'] = input_old_index
    devices[index]['new_index'] = input_new_index
    print(f"Thiết bị {input_id} đã được cập nhật")
    logging.info("The index has been successfully updated.")

def orverload_warning(devices):
    input_id = input("Nhập mã ID thiết bị: ").strip().upper()
    if not input_id:
        print("Mã ID không hợp lệ (không được để trống)")
        logging.error("Invalid device code")
        return 
    index = check_id(devices,input_id)

    if index == -1:
        print("Lỗi: (ERR-E01): Mã thiết bị này không tồn tại trong danh sách hệ thống")
        logging.error("The device is not in the system.")
        return
    device = devices[index]

    if device['status'] == "Overload":
        print("[Lỗi] (ERR-E04): Thao tác bị hủy! Thiết bị này đã được kích hoạt trạng thái OVERLOAD từ trước!")
        logging.error("The device is overloaded.")
        return
    
    if device['new_index'] - device['old_index'] >= 5000:
        devices[index]['status'] = 'Overload'
        logging.warning(f"Device {input_id} has exceeded the safe consumption limit, switching to OVERLOAD mode!")
        print(f"Tìm thấy thiết bị tại: {devices[index]['location']} Lượng tiêu thụ:({device['new_index'] - device['old_index']})kWh")
        print("[Thành công]: Thiết bị M01 đã được kích hoạt trạng thái OVERLOAD!")
def total_price_electronic(devices):
    total_index = 0
    total_money = 0
    percent_rate = 3
    for value in devices:
        total_index += value['new_index'] - value['old_index']
    if total_index >= 50000:
        total_money = total_index*3000*1.03
    else:
        total_money = total_index*3000
    return total_money,total_index,percent_rate

def menu_main():
    while True:
        print("""
SMART ENERGY MONITOR - PHONG CO ĐIEN
1. Xem danh sách thiêt bị giám sát
2. Cập nhật chỉ sô điện tiêu thụ (Check-in)
3. Kích hoạt trạng thái cảnh báo quá tải
4. Tính tổng Lượng điện & Chi phí năng lượng
5. Thoát chương trình.
    """)
        choice = input("Mời chọn chức năng (1-5): ")
        match choice:
            case '1':
                display_info(devices)
            case '2':
                update_indices(devices)
            case '3':
                orverload_warning(devices)
            case '4':
                total_money,total_index,percent=total_price_electronic(devices)
                print("-- BÁO CÁO TÀI CHÍNH NĂNG LƯỢNG")
                print(f"Tổng lượng điện tiêu thụ thực tế :{total_index}kWh")
                print(f"Tỷ lệ chiết khấu áp dụng từ nhà nước:{percent}%")
                print(f"Tổng chi phí năng lượng phải trả sau chiết khấu :{total_money:,} VND")
            case '5':
                print("Thoát chương trình")
                break
            case _:
                print("[Lỗi] (ERR-E05): Lựa chọn sai! Vui lòng nhập đúng số thứ tự chức năng từ 1 đến 5!")
                logging.warning("The user is trying to enter a number different from 1 to 5.")

menu_main()
