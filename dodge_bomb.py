import os
import random
import sys
import pygame as pg
import time


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 演習1
def gameover(screen: pg.Surface) -> None:
    """
    ゲームオーバー画面を表示する関数
    引数：描画先のscreen Surface
    """
    black_img = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(black_img, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
    black_img.set_alpha(150) 
    screen.blit(black_img, [0, 0])

    font_o = pg.font.Font(None, 80)
    txt = font_o.render("Game Over", True, (255, 255, 255))
    screen.blit(txt, [WIDTH//2 - 150, HEIGHT//2])

    kk_cry = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    screen.blit(kk_cry, [WIDTH//2 - 250, HEIGHT//2 - 20])
    screen.blit(kk_cry, [WIDTH//2 + 200, HEIGHT//2 - 20])

    pg.display.update()
    time.sleep(5)

# 演習２
def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    時間経過で拡大する爆弾のリストと加速度のリストを生成する関数
    戻り値：(爆弾Surfaceのリスト, 加速度のリスト)
    """
    bb_imgs = []
    bb_accs = [a for a in range(1, 11)] 
    
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_img.set_colorkey((0, 0, 0))
        bb_imgs.append(bb_img)
        
    return bb_imgs, bb_accs



def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRect or 爆弾Rect
    戻り値：判定結果タプル（横方向判定結果，縦方向判定結果）
    True：画面内/False：画面外
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:  # 横方向判定
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:  # 縦方向判定
        tate = False
    return yoko, tate

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bb_img = pg.Surface((20, 20))
    bb_img.set_colorkey((0, 0, 0))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_rct = bb_img.get_rect() 
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = +5, +5 

    # 演習課題２
    bb_imgs, bb_accs = init_bb_imgs()
    bb_rct = bb_imgs[0].get_rect() 
    
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return

        if kk_rct.colliderect(bb_rct):  # こうかとんRectと爆弾Rectが重なったら
            gameover(screen)
            print("ゲームオーバー")
            return
        
        # 演習課題２
        idx = min(tmr // 500, 9)
        current_bb_img = bb_imgs[idx]
        avx = vx * bb_accs[idx]
        avy = vy * bb_accs[idx]
        bb_rct.width = current_bb_img.get_rect().width
        bb_rct.height = current_bb_img.get_rect().height
        bb_rct.move_ip(avx, avy) # 加速された速度で移動させる
        screen.blit(current_bb_img, bb_rct) # 描画するときは現在のサイズの画像を使う
        tmr += 1
        
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0] 
                sum_mv[1] += mv[1]

        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)


        bb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # 横方向にはみ出ていたら
            vx *= -1
        if not tate:  # 縦方向にはみ出ていたら
            vy *= -1

        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
