import pygame as pg
import numpy as np
import random as r

def Main():

  # 初期化処理
  chip_s = 48  # マップチップの基本サイズ
  map_s = pg.Vector2(32, 17)  # マップの横・縦の配置数

  pg.init()
  pg.display.set_caption('ぼくのかんがえたさいきょうのげーむ II')
  disp_w = int(chip_s * map_s.x)
  disp_h = int(chip_s * map_s.y)
  screen = pg.display.set_mode((disp_w, disp_h))
  clock = pg.time.Clock()
  font = pg.font.Font(None, 15)
  frame = 0
  exit_flag = False
  exit_code = '000'
  bulletMAX = 100
  bulletPos = []
  bulletAddCtrl = False
  bulletDecay = 1.1  # 弾の減衰率(1以上は加速)
  bulletOrgSpeed = 5
  bulletSpeed = []
  bulletMaxTime = 50
  bulletTime = []
  bulletMOA = 100  # MOAとは集弾率のこと 今回は高いほど集団率が悪い
  bulletROF = 4  # フレームあたりの発射レート
  bulletDirTemp = []
  bulletDirRecip = 0.0

  background_img = pg.image.load(f'data/img/map-background.png')
  background_s = pg.Vector2(48, 48)

  # グリッド設定
  grid_cx = '#ff0000'
  grid_cy = '#0000ff'

  # 自キャラ移動関連
  cmdWMove = False  # Wキー移動コマンドの管理変数
  cmdAMove = False  # Aキー移動コマンドの管理変数
  cmdSMove = False  # Sキー移動コマンドの管理変数
  cmdDMove = False  # Dキー移動コマンドの管理変数
  cmd_move = -1  # 移動コマンドの総合管理変数
  m_vec = [
      pg.Vector2(0, -0.2),
      pg.Vector2(0.2, 0),
      pg.Vector2(0, 0.2),
      pg.Vector2(-0.2, 0)
  ]  # 移動コマンドに対応したXYの移動量

  # 自キャラの画像読込み
  reimu_p = pg.Vector2(2, 3)   # 自キャラ位置
  reimu_s = pg.Vector2(48, 64)  # 画面に出力する自キャラサイズ 48x64
  reimu_d = 2  # 自キャラの向き
  reimu_img_raw = pg.image.load('./data/img/reimu.png')
  reimu_img_arr = []
  for i in range(4):   # 上右下左の4方向
    reimu_img_arr.append([])
    for j in range(3):  # アニメーションパターンx3
      p = pg.Vector2(24 * j, 32 * i)  # 切り抜きの開始座標・左上
      tmp = reimu_img_raw.subsurface(pg.Rect(p, (24, 32)))  # 切り出し
      tmp = pg.transform.scale(tmp, reimu_s)  # 拡大
      reimu_img_arr[i].append(tmp)
    reimu_img_arr[i].append(reimu_img_arr[i][1])

    # 弾画像の読み込み
  bullet = pg.image.load("Data/img/bullet.png")

  # 弾の追加
  def BulletAdd():

    bulletDirTemp = pg.mouse.get_pos()
    bulletDirTemp -= (dp + [24, 36])
    bulletDirTemp += [r.randint(-bulletMOA, bulletMOA),
                      r.randint(-bulletMOA, bulletMOA)]
    bulletDirRecip = 1 / np.sqrt(bulletDirTemp[0]**2 + bulletDirTemp[1]**2)
    for i in range(len(bulletDirTemp)):
      bulletDirTemp[i] *= bulletDirRecip * bulletOrgSpeed

    if frame % bulletROF == 0:
      bulletPos.append(dp + [0, 12])
      bulletTime.append(bulletMaxTime)
      bulletSpeed.append(bulletDirTemp)
    if len(bulletPos) >= bulletMAX:
      bulletPos.pop(0)

  # 弾の動き
  def BulletMove():

    for i in range(len(bulletPos)):
      bulletPos[i] += bulletSpeed[i]
      for j in range(len(bulletSpeed[i])):
        bulletSpeed[i][j] *= bulletDecay
        bulletTime[i] -= 1

    if len(bulletTime) != 0:
      if bulletTime[0] <= 0:
        bulletPos.pop(0)
        bulletSpeed.pop(0)
        bulletTime.pop(0)

  # ゲームループ
  while not exit_flag:

    # システムイベントの検出
    for event in pg.event.get():
      if event.type == pg.QUIT:  # ウィンドウ[X]の押下
        exit_flag = True
        exit_code = '001'
      # 移動操作の「キー離し」の受け取り処理
      if event.type == pg.KEYUP:
        if event.key == pg.K_w:
          cmdWMove = False
        if event.key == pg.K_a:
          cmdAMove = False
        if event.key == pg.K_s:
          cmdSMove = False
        if event.key == pg.K_d:
          cmdDMove = False
      # 移動操作の「キー入力」の受け取り処理
      if event.type == pg.KEYDOWN:
        if event.key == pg.K_w:
          cmdWMove = True
        if event.key == pg.K_a:
          cmdAMove = True
        if event.key == pg.K_s:
          cmdSMove = True
        if event.key == pg.K_d:
          cmdDMove = True

      # マウスクリック/クリック離しの受け取り処理
      if event.type == pg.MOUSEBUTTONDOWN:
        bulletAddCtrl = True
      elif event.type == pg.MOUSEBUTTONUP:
        bulletAddCtrl = False

    # 背景描画
    screen.fill(pg.Color('WHITE'))

    # 地面描画
    for x in range(0, disp_w, int(background_s.x)):
      for y in range(0, disp_h, int(background_s.y)):
        screen.blit(background_img, (x, y))

    # グリッド
    for x in range(0, disp_w, chip_s):  # 縦線
      pg.draw.line(screen, grid_cx, (x, 0), (x, disp_h))
    for y in range(0, disp_h, chip_s):  # 横線
      pg.draw.line(screen, grid_cy, (0, y), (disp_w, y))

    # 移動コマンドの処理
    if cmdWMove == True:
      cmd_move = 0
    elif cmdDMove == True:
      cmd_move = 1
    elif cmdSMove == True:
      cmd_move = 2
    elif cmdAMove == True:
      cmd_move = 3
    else:
      cmd_move = -1

    if cmd_move != -1:
      reimu_d = cmd_move  # キャラクタの向きを更新
      af_pos = reimu_p + m_vec[cmd_move]  # 移動後の (仮) 座標
      if (0 <= af_pos.x <= map_s.x - 1) and (0 <= af_pos.y <= map_s.y - 1):
        reimu_p += m_vec[cmd_move]  # 画面外に移動しないなら実際のキャラを移動

    # 弾の生成
    if bulletAddCtrl == True:
      BulletAdd()

    # 自キャラの描画 dp:描画基準点（imgの左上座標）
    dp = reimu_p * chip_s - pg.Vector2(0, 24)
    af = frame // 6 % 4  # 6フレーム毎にアニメーション
    screen.blit(reimu_img_arr[reimu_d][af], dp)

    # 弾の描画
    for i in range(len(bulletPos)):
      screen.blit(bullet, bulletPos[i])

    # 弾の移動
    BulletMove()

    # フレームカウンタの描画
    frame += 1
    frm_str = f'{frame:05}'
    screen.blit(font.render(frm_str, True, 'BLACK'), (10, 10))
    screen.blit(font.render(f'{reimu_p}', True, 'BLACK'), (10, 20))

    # 画面の更新と同期
    pg.display.update()
    clock.tick(30)

  # ゲームループ [ここまで]
  pg.quit()
  return exit_code

if __name__ == "__main__":
  code = Main()
  print(f'プログラムを「コード{code}」で終了しました。')
