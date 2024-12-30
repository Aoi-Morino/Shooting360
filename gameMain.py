import pygame as pg

def main():

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

  background_img = pg.image.load(f'data/img/map-background.png')
  background_s = pg.Vector2(48, 48)

  # グリッド設定
  grid_cx = '#ff0000'
  grid_cy = '#0000ff'

  # 自キャラ移動関連
  cmd_move = -1  # 移動コマンドの管理変数
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

  # ゲームループ
  while not exit_flag:

    # システムイベントの検出
    for event in pg.event.get():
      if event.type == pg.QUIT:  # ウィンドウ[X]の押下
        exit_flag = True
        exit_code = '001'
      # 移動操作の「キー離し」の受け取り処理
      if event.type == pg.KEYUP:
        if event.key == pg.K_w and cmd_move == 0:
          cmd_move = -1
        elif event.key == pg.K_d and cmd_move == 1:
          cmd_move = -1
        elif event.key == pg.K_s and cmd_move == 2:
          cmd_move = -1
        elif event.key == pg.K_a and cmd_move == 3:
          cmd_move = -1
      # 移動操作の「キー入力」の受け取り処理
      if event.type == pg.KEYDOWN:
        if event.key == pg.K_w:
          cmd_move = 0
        elif event.key == pg.K_d:
          cmd_move = 1
        elif event.key == pg.K_s:
          cmd_move = 2
        elif event.key == pg.K_a:
          cmd_move = 3

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
    if cmd_move != -1:
      reimu_d = cmd_move  # キャラクタの向きを更新
      af_pos = reimu_p + m_vec[cmd_move]  # 移動後の (仮) 座標
      if (0 <= af_pos.x <= map_s.x - 1) and (0 <= af_pos.y <= map_s.y - 1):
        reimu_p += m_vec[cmd_move]  # 画面外に移動しないなら実際のキャラを移動

    # 自キャラの描画 dp:描画基準点（imgの左上座標）
    dp = reimu_p * chip_s - pg.Vector2(0, 24)
    af = frame // 6 % 4  # 6フレーム毎にアニメーション
    screen.blit(reimu_img_arr[reimu_d][af], dp)

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
  code = main()
  print(f'プログラムを「コード{code}」で終了しました。')
