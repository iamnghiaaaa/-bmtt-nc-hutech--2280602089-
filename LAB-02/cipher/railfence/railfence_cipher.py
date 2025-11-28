class RailFenceCipher:
    def __init__(self):
        pass

    def rail_fence_encrypt(self, plain_text, num_rails):
        rails = [[] for _ in range(num_rails)]
        rail_index = 0
        direction = 1  # 1: down, -1: up
        
        # Viết các ký tự theo đường zigzag lên các rail
        for char in plain_text:
            rails[rail_index].append(char)
            if rail_index == 0:
                direction = 1
            elif rail_index == num_rails - 1:
                direction = -1
            rail_index += direction
            
        # Nối các ký tự trong từng rail lại để tạo ra ciphertext
        cipher_text = ''.join(''.join(rail) for rail in rails)
        return cipher_text

    def rail_fence_decrypt(self, cipher_text, num_rails):
        # 1. Xác định độ dài (số ký tự) của từng rail
        rail_lengths = [0] * num_rails
        rail_index = 0
        direction = 1

        for _ in range(len(cipher_text)):
            rail_lengths[rail_index] += 1
            if rail_index == 0:
                direction = 1
            elif rail_index == num_rails - 1:
                direction = -1
            rail_index += direction

        # 2. Chia ciphertext thành các rail dựa trên độ dài đã xác định
        rails = []
        start = 0
        for length in rail_lengths:
            rails.append(cipher_text[start:start + length])
            start += length
        
        # 3. Đọc plaintext bằng cách zigzag qua các rail
        plain_text = ""
        rail_index = 0
        direction = 1

        for _ in range(len(cipher_text)):
            # Lấy ký tự đầu tiên từ rail hiện tại
            plain_text += rails[rail_index][0]
            # Xóa ký tự vừa lấy khỏi rail
            rails[rail_index] = rails[rail_index][1:]

            # Thay đổi hướng zigzag
            if rail_index == 0:
                direction = 1
            elif rail_index == num_rails - 1:
                direction = -1
            rail_index += direction

        return plain_text