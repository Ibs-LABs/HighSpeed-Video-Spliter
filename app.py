import cv2
import os
import multiprocessing

select_fps = 60

def spliter(start, end, file_name):
    video = cv2.VideoCapture(os.path.join('.', 'raw', file_name))
    video.set(cv2.CAP_PROP_POS_FRAMES, start)
    
    for frame_n in range(start, end):
        ret, frame = video.read()
        if not ret:
            break

        if frame_n % select_fps == 0:
            cv2.imwrite(os.path.join('.', 'result', file_name + '-' + str(frame_n) + '.png'), frame)

    video.release()

def file_selector(file_name):
    video = cv2.VideoCapture(os.path.join('.', 'raw', file_name))
    
    total_frame = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    print('Total frame : ' + str(total_frame))
    
    video.release()

    core_spliter = total_frame // os.cpu_count()
    
    process_list = []
    for for_a in range(os.cpu_count()):
        if for_a == os.cpu_count() - 1:
            process = multiprocessing.Process(target = spliter, args = (core_spliter * for_a, total_frame + 1, file_name))
        else:
            process = multiprocessing.Process(target = spliter, args = (core_spliter * for_a, core_spliter * (for_a + 1), file_name))

        process.start()
        process_list.append(process)

    for process in process_list:
        process.join()

if __name__ == '__main__':
    if not os.path.exists(os.path.join('.', 'result')):
        os.mkdir(os.path.join('.', 'result'))

    for for_a in os.listdir(os.path.join('.', 'raw')):
        print(for_a)

        _, ext = os.path.splitext(for_a)
        print(ext)

        if ext in ('.avi', '.mp4'):
            file_selector(for_a)