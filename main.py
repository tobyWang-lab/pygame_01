#sprite->遊戲中的元素
import pygame
import random
import os
from PIL import Image

from pygame import rect
from pygame.constants import KEYDOWN

FPS = 60
WIDTH=500
HEIGHT=600

BLACK=(0,0,0)
WHITE=(255,255,255)
GREEN=(0,255,0)
RED=(255,0,0)
BLUE=(0,0,255)

# 遊戲初始化
pygame.init()

# 創建遊戲視窗，pygame.display.set_mode((寬度,高度))
screen=pygame.display.set_mode((WIDTH,HEIGHT))

#編輯遊戲視窗上方名稱
pygame.display.set_caption("第一個遊戲")

# 對時間進行管控
clock=pygame.time.Clock()

# 載入圖片(必須在遊戲初始化後才能載入圖片)
# 切割背景圖片
img=Image.open(os.path.join("img","backgroung.jpg"))
print(img.size)
cut_img = img.crop((1000,600,1000+WIDTH,600+HEIGHT)) # (左、上、又、下)
cut_img.save(os.path.join("img","cut_backgroung.jpg"))
# convert會將載入的圖片轉換成pygame容易讀取的格式
# background_img = pygame.image.load(os.path.join("img","backgroung.jpg")).convert()
background_img = pygame.image.load(os.path.join("img","cut_backgroung.jpg")).convert()
player_img = pygame.image.load(os.path.join("img","aircraft.png")).convert()
# rock_img = pygame.image.load(os.path.join("img","rock.png")).convert()
bullet_img = pygame.image.load(os.path.join("img","meteorite.png")).convert()
rock_imgs=[]
for i in range(4):
	rock_imgs.append(pygame.image.load(os.path.join("img",f"rock{i}.png"),).convert())

# 設定遊戲中的物件
class Player(pygame.sprite.Sprite):
	def __init__(self):
        # call sprite內建初始涵式
		pygame.sprite.Sprite.__init__(self)
        # # 定義所需顯示的圖片，下圖為pygame預設的平面 
		# self.image=pygame.Surface((50,40))
		# self.image.fill(GREEN)

		# 放入設置好的圖片，並從新定義圖片長寬
		# pygame.transform.scale(圖片,大小)
		self.image=pygame.transform.scale(player_img,(40,40))
		# 將指定的顏色透明化，self.image.set_colorkey((R,G,B)))
		self.image.set_colorkey(BLACK) 
        # 定位圖片位置，將圖片框起來
		self.rect=self.image.get_rect()
		# 當碰撞判斷為圓型時，要設置半徑大小，並將圓形畫出來測試看看並調整，測試完即可註解掉
		self.radius=self.rect.width/2*0.9
		# pygame.draw.circle(self.image,GREEN, self.rect.center, self.radius)
        # 設定圖片位置，下方xy為圖片左上角的座標，整個遊戲框架的左上角為(0,0)
		self.rect.centerx = WIDTH/2
		self.rect.bottom = HEIGHT-10
		self.speedxy = 8
        # 將圖片設置在中央
        # self.rect.center=(WIDTH/2,HEIGHT/2)
	def update(self):
		# get_pressed()會回傳一連串boolean值，有按則為True，反之則為False
		# K_RIGHT即為右鍵、K_a即為a鍵、K_SPACE即為空白鍵
		key_pressed=pygame.key.get_pressed()
		if key_pressed[pygame.K_RIGHT]:
			self.rect.x += self.speedxy
		if key_pressed[pygame.K_LEFT]:
			self.rect.x -= self.speedxy
		if key_pressed[pygame.K_UP]:
			self.rect.y -= self.speedxy
		if key_pressed[pygame.K_DOWN]:
			self.rect.y += self.speedxy
		
		if self.rect.right>WIDTH :
			self.rect.right=WIDTH
		if self.rect.left<0:
			self.rect.left=0
		if self.rect.bottom>HEIGHT:
			self.rect.bottom=HEIGHT
		if self.rect.top<0:
			self.rect.top=0
	def shoot(self):
		bullet=Bullet(self.rect.centerx,self.rect.top)
		all_sprites.add(bullet)
		bullets.add(bullet)

class Rock(pygame.sprite.Sprite):
	def __init__(self):
        # call sprite內建初始涵式
		pygame.sprite.Sprite.__init__(self)
		self.image_ori = pygame.transform.scale(random.choice(rock_imgs),(50,50))
		self.image_ori.set_colorkey(BLACK)
		self.image=self.image_ori.copy()
        # 定位圖片位置，將圖片框起來
		self.rect=self.image.get_rect()
		# 當碰撞判斷為圓型時，要設置半徑大小，並將圓形畫出來測試看看並調整，測試完即可註解掉
		self.radius=self.rect.width/2*0.7
		# pygame.draw.circle(self.image_ori, GREEN, self.rect.center, self.radius)
        # 設定圖片位置，下方xy為圖片左上角的座標，整個遊戲框架的左上角為(0,0)
		self.rect.x = random.randrange(0,WIDTH-self.rect.width)
		self.rect.y = random.randrange(-100,-40)
		self.speedy = random.randrange(2,6)
		self.speedx =random.randrange(-3,3)
        # 將圖片設置在中央
        # self.rect.center=(WIDTH/2,HEIGHT/2)
		# 設置圖片每次更新轉的角度
		self.total_degree=0
		self.rot_degree=random.randrange(-3,3)
	
	# 透過函式將圖片旋轉
	def rotate(self):
		# pygame.transform.rotate(要旋轉的圖片,旋轉角度)
		# 但由於轉動會有細微失真，更新的時候會使失真疊加導致圖片呈現不良
		# 故要使失真不進行累加
		# 為此在輸入照片地方在copy一份，並讓沒有失真的圖進行轉動
		self.total_degree +=self.rot_degree
		self.total_degree=self.total_degree%360
		self.image = pygame.transform.rotate(self.image_ori,self.total_degree)
		# 轉動時因都無重新定位，故轉動時會很奇怪
		# 紀錄原先的中心定位
		center = self.rect.center
		# 取得新的定位
		self.rect = self.image.get_rect()
		# 將新定位的中心更新原有的紀錄
		self.rect.center = center


	def update(self):
		self.rotate()
		self.rect.y += self.speedy
		self.rect.x += self.speedx
		if self.rect.top>HEIGHT or self.rect.left>WIDTH or self.rect.right<0:
			self.rect.x = random.randrange(0,WIDTH-self.rect.width)
			self.rect.y = random.randrange(-100,-40)
			self.speedy = random.randrange(2,6)
			self.speedx =random.randrange(-3,3)

class Bullet(pygame.sprite.Sprite):
	def __init__(self,x,y):
        # call sprite內建初始涵式
		pygame.sprite.Sprite.__init__(self)
        # 定義所需顯示的圖片，下圖為pygame預設的平面 
		self.image=pygame.transform.scale(bullet_img,(20,20))
		self.image.set_colorkey(WHITE)
        # 定位圖片位置，將圖片框起來
		self.rect=self.image.get_rect()
        # 設定圖片位置，下方xy為圖片左上角的座標，整個遊戲框架的左上角為(0,0)
		self.rect.centerx = x 
		self.rect.bottom = y
		self.speedy = -10
        # 將圖片設置在中央
        # self.rect.center=(WIDTH/2,HEIGHT/2)
	def update(self):
		self.rect.y += self.speedy
		if self.rect.bottom<0:
			# kill()是sprite的函式之一，此函式會將此sprite從sprite群組中移除
			self.kill()

# 將遊戲中的物件加入至sprite群組當中
all_sprites=pygame.sprite.Group()
rocks=pygame.sprite.Group()
bullets=pygame.sprite.Group()
player=Player()
all_sprites.add(player)
for i in range(8):
	r=Rock()
	all_sprites.add(r)
	rocks.add(r)
running=True

# 遊戲迴圈
while running:
	# 此處代表一秒鐘最多只能執行幾次,也相當於帪數(一秒更新幾次畫面)
	clock.tick(FPS)

# 取得輸入，因為可能輸入同時會有多個，故需要用for迴圈全部讀出來
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			running=False
		elif event.type== pygame.KEYDOWN:
			# KEYDOWN代表按下鍵盤
			if event.key==pygame.K_SPACE:
				player.shoot()



# 更新遊戲
	#取得sprite群組裡所有物件的update函式
	all_sprites.update()
	# pygame.sprite.groupcollide可以判斷出兩個群組裡的sprite有無碰撞，
	# 並回傳一個dictionary，裡面包括了兩個群組裡碰撞的sprite
	# pygame.sprite.groupcollide(群組1,群組2,碰撞後群組1裡的sprite是否要kill(),碰撞後群組1裡的sprite是否要kill(),使用圓形判斷預設為矩形)
	# 此函式的碰撞判斷是使用舉行
	hits=pygame.sprite.groupcollide(rocks,bullets,True,True)
	for hits in hits:
		r=Rock()
		all_sprites.add(r)
		rocks.add(r)
	# 在pygame.sprite.spritecollide函式中加入參數pygame.sprite.collide_circle代表碰撞判斷是用圓形，預設為矩形
	# 此外，加入此參數後要在物件1和群組2中加入圓形的半徑參數self.radius
	hits = pygame.sprite.spritecollide(player,rocks,False,pygame.sprite.collide_circle)
	if hits:
		running = False
# 畫面顯示
	# 將畫面填滿，三個參數分別為R、G、B，範圍都是0~255
	# screen.fill((R,G,B))
	screen.fill(BLACK)
	# 將圖放在畫面上
	# screen.blit(放置圖片，位置)
	screen.blit(background_img, (0,0))
	# 將sprite群組裡所有遊戲物件放置在螢幕上
	all_sprites.draw(screen)
# 更新畫面
	pygame.display.update()
# 關閉
pygame.quit()