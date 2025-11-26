import time
import random

# ★ 메인 서버(main.py)에서 호출하는 함수
def train_model(config, callback=None):
    print(f"   [Train.py] 모델 학습 시작... 설정값: {config}")
    
    # 1. 설정값 가져오기
    epochs = config.get('epochMax', 100)
    model_name = config.get('model', 'Unknown')
    
    # 2. 학습 루프 (여기서 실제 학습인 척 함)
    best_acc = 0.0
    final_loss = 1.0
    
    for epoch in range(1, epochs + 1):
        # ★ 전시회용 속도 조절 (너무 빠르면 안 보이니까 0.05초)
        time.sleep(0.05)
        
        # 가짜 데이터 생성 (점점 똑똑해지는 척)
        noise = random.uniform(-0.02, 0.02)
        
        # 초반엔 Loss가 높고, 뒤로 갈수록 줄어드는 수식
        loss = max(0.01, 1.0 - (epoch / epochs)) + noise
        
        # 초반엔 Acc가 낮고, 뒤로 갈수록 99%까지 올라가는 수식
        acc = min(99.5, 40 + (epoch / epochs) * 59) + (noise * 10)
        
        if acc > best_acc:
            best_acc = acc
        final_loss = loss

        # ★ [핵심] 메인 서버(main.py)한테 "나 지금 이만큼 했어!"라고 보고함
        if callback:
            callback(epoch, loss, acc)
            
    print(f"   [Train.py] 학습 완료! Best Acc: {best_acc:.2f}%")

    # 3. 최종 결과 리턴 (결과 화면에 뿌려질 데이터)
    return {
        "best_acc": round(best_acc, 2),
        "final_loss": round(final_loss, 4),
        "best_epoch": epochs - random.randint(1, 5)
    }