
import numpy as np
import pyautogui

# Inicialização da tela do Paintm
pyautogui.hotkey('win', 'r')
pyautogui.write('mspaint')
pyautogui.press('enter')
pyautogui.sleep(2)

# Configurações
lower_skin = np.array([0, 20, 70], dtype=np.uint8)
upper_skin = np.array([20, 255, 255], dtype=np.uint8)
brush_color = (0, 0, 255)  # Vermelho
brush_radius = 5

# Captura de vídeo da webcam
cap = cv2.VideoCapture(0)

# Loop principal
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Conversão para HSV
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Detecção da região de interesse (dedo)
    mask = cv2.inRange(hsv_frame, lower_skin, upper_skin)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # Encontrar contornos na máscara
    contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Encontrar o maior contorno (dedo)
        max_contour = max(contours, key=cv2.contourArea)
        if cv2.contourArea(max_contour) > 1000:
            # Encontrar o centro do contorno
            M = cv2.moments(max_contour)
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])

            # Simular o clique do mouse para desenhar no Paint
            pyautogui.moveTo(cx, cy)
            pyautogui.click()
            pyautogui.sleep(0.1)

    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
