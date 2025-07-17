from ultralytics import YOLO
import multiprocessing



import multiprocessing

if __name__ == '__main__':
    multiprocessing.freeze_support()  # 윈도우 exe 배포용. 생략 가능.
    
    model = YOLO('yolov8s-seg.pt')

    model.train(
        data    = 'C:/Users/cho-j/OneDrive/바탕 화면/Ecoli_2025/data.yaml',
        imgsz   = 256,
        epochs  = 50,
        batch   = 8,
        lr0     = 1e-3,          # 초기 learning rate
        lrf     = 0.01,          # (선택) final lr = lr0 * lrf
        device  = 0,             # GPU 사용
        project = 'C:/Users/cho-j/OneDrive/바탕 화면/Ecoli_2025/runs',
        name    = 'exp_seg_colab'
    )

    
    # 멀티프로세싱 관련 코드나 모델 학습 코드 작성
    # 예) torch.multiprocessing, DataLoader(num_workers>0) 등
