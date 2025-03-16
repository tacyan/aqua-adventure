"""
アクアアドベンチャー - 水中2Dアクションゲーム

このゲームは、水中を冒険する2Dアクションゲームです。
プレイヤーは水中を自由に泳ぎ回り、障害物を避けながら宝物を集め、
敵と戦いながらステージをクリアしていきます。

Author: Claude
Version: 1.0.0
"""

import pygame
import sys
from typing import List, Dict, Optional
from .player import Player
from .enemy import Enemy, Jellyfish
from .game_state import GameState, SceneManager

# 定数定義
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# 色の定数
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

class Game:
    """
    ゲームの主要クラス
    
    ゲームの初期化、メインループ、状態管理を行います。
    """
    
    def __init__(self) -> None:
        """
        ゲームの初期化を行います。
        Pygameの設定、画面の作成、ゲーム状態の初期化を実施します。
        """
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("アクアアドベンチャー")
        self.clock = pygame.time.Clock()
        self.isRunning = True
        
        # シーンマネージャーの初期化
        self.sceneManager = SceneManager()
        self.setupScenes()
        
        # ゲームオブジェクトの初期化
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.enemies: List[Enemy] = []
        self.setupEnemies()
        
        # スプライトグループの設定
        self.allSprites = pygame.sprite.Group()
        self.allSprites.add(self.player)
        for enemy in self.enemies:
            self.allSprites.add(enemy)
    
    def setupScenes(self) -> None:
        """
        各シーンの処理ハンドラを登録します。
        """
        self.sceneManager.registerHandlers(
            GameState.TITLE,
            self.updateTitle,
            self.renderTitle
        )
        self.sceneManager.registerHandlers(
            GameState.PLAYING,
            self.updatePlaying,
            self.renderPlaying
        )
        self.sceneManager.registerHandlers(
            GameState.PAUSED,
            self.updatePaused,
            self.renderPaused
        )
        self.sceneManager.registerHandlers(
            GameState.GAME_OVER,
            self.updateGameOver,
            self.renderGameOver
        )
    
    def setupEnemies(self) -> None:
        """
        敵キャラクターを初期配置します。
        """
        # テスト用にクラゲを配置
        self.enemies.append(Jellyfish(200, 200))
        self.enemies.append(Jellyfish(600, 400))
    
    def handleEvents(self) -> None:
        """
        Pygameのイベントを処理します。
        キー入力、ウィンドウクローズなどのイベントを処理します。
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.isRunning = False
            elif event.type == pygame.KEYDOWN:
                self.handleKeyDown(event.key)
    
    def handleKeyDown(self, key: int) -> None:
        """
        キー入力を処理します。
        
        Args:
            key (int): 押されたキーのコード
        """
        if self.sceneManager.getCurrentState() == GameState.TITLE:
            if key == pygame.K_SPACE:
                self.sceneManager.changeState(GameState.PLAYING)
        elif self.sceneManager.getCurrentState() == GameState.PLAYING:
            if key == pygame.K_ESCAPE:
                self.sceneManager.changeState(GameState.PAUSED)
        elif self.sceneManager.getCurrentState() == GameState.PAUSED:
            if key == pygame.K_ESCAPE:
                self.sceneManager.changeState(GameState.PLAYING)
            elif key == pygame.K_q:
                self.sceneManager.changeState(GameState.TITLE)
        elif self.sceneManager.getCurrentState() == GameState.GAME_OVER:
            if key == pygame.K_SPACE:
                self.sceneManager.changeState(GameState.TITLE)
    
    def updateTitle(self) -> None:
        """
        タイトル画面の更新処理を行います。
        """
        pass
    
    def updatePlaying(self) -> None:
        """
        ゲームプレイ中の更新処理を行います。
        """
        # プレイヤーの更新
        self.player.update()
        
        # 敵の更新
        for enemy in self.enemies:
            enemy.update(self.player.position)
        
        # 衝突判定
        self.checkCollisions()
    
    def updatePaused(self) -> None:
        """
        ポーズ中の更新処理を行います。
        """
        pass
    
    def updateGameOver(self) -> None:
        """
        ゲームオーバー時の更新処理を行います。
        """
        pass
    
    def renderTitle(self, screen: pygame.Surface) -> None:
        """
        タイトル画面を描画します。
        
        Args:
            screen (pygame.Surface): 描画対象の画面
        """
        screen.fill(BLUE)
        
        font = pygame.font.Font(None, 74)
        title = font.render("アクアアドベンチャー", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/3))
        screen.blit(title, title_rect)
        
        font = pygame.font.Font(None, 36)
        start = font.render("Press SPACE to Start", True, WHITE)
        start_rect = start.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT*2/3))
        screen.blit(start, start_rect)
    
    def renderPlaying(self, screen: pygame.Surface) -> None:
        """
        ゲームプレイ中の画面を描画します。
        
        Args:
            screen (pygame.Surface): 描画対象の画面
        """
        screen.fill(BLUE)
        
        # スプライトの描画
        self.allSprites.draw(screen)
        
        # プレイヤーの泡の描画
        for bubble in self.player.bubbles:
            screen.blit(bubble.image, bubble.rect)
        
        # UIの描画
        self.renderUI(screen)
    
    def renderPaused(self, screen: pygame.Surface) -> None:
        """
        ポーズ画面を描画します。
        
        Args:
            screen (pygame.Surface): 描画対象の画面
        """
        # ゲーム画面を背景として描画
        self.renderPlaying(screen)
        
        # 半透明の黒いオーバーレイ
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(128)
        screen.blit(overlay, (0, 0))
        
        # ポーズメニューの描画
        font = pygame.font.Font(None, 74)
        pause = font.render("PAUSE", True, WHITE)
        pause_rect = pause.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/3))
        screen.blit(pause, pause_rect)
        
        font = pygame.font.Font(None, 36)
        resume = font.render("Press ESC to Resume", True, WHITE)
        resume_rect = resume.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT*2/3))
        screen.blit(resume, resume_rect)
        
        quit_text = font.render("Press Q to Quit", True, WHITE)
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT*2/3 + 40))
        screen.blit(quit_text, quit_rect)
    
    def renderGameOver(self, screen: pygame.Surface) -> None:
        """
        ゲームオーバー画面を描画します。
        
        Args:
            screen (pygame.Surface): 描画対象の画面
        """
        screen.fill(BLACK)
        
        font = pygame.font.Font(None, 74)
        game_over = font.render("GAME OVER", True, WHITE)
        game_over_rect = game_over.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/3))
        screen.blit(game_over, game_over_rect)
        
        font = pygame.font.Font(None, 36)
        restart = font.render("Press SPACE to Restart", True, WHITE)
        restart_rect = restart.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT*2/3))
        screen.blit(restart, restart_rect)
    
    def renderUI(self, screen: pygame.Surface) -> None:
        """
        ゲーム中のUIを描画します。
        
        Args:
            screen (pygame.Surface): 描画対象の画面
        """
        # HPバー
        self.drawBar(screen, 10, 10, self.player.hp, self.player.maxHp,
                    (255, 0, 0), "HP")
        
        # スタミナバー
        self.drawBar(screen, 10, 40, self.player.stamina, self.player.maxStamina,
                    (0, 255, 0), "スタミナ")
        
        # 酸素バー
        self.drawBar(screen, 10, 70, self.player.oxygen, self.player.maxOxygen,
                    (0, 0, 255), "酸素")
    
    def drawBar(self, screen: pygame.Surface, x: int, y: int,
                value: float, maxValue: float, color: tuple,
                label: str) -> None:
        """
        ステータスバーを描画します。
        
        Args:
            screen (pygame.Surface): 描画対象の画面
            x (int): X座標
            y (int): Y座標
            value (float): 現在値
            maxValue (float): 最大値
            color (tuple): バーの色
            label (str): バーのラベル
        """
        BAR_WIDTH = 200
        BAR_HEIGHT = 20
        
        # バーの背景
        pygame.draw.rect(screen, (128, 128, 128),
                        (x, y, BAR_WIDTH, BAR_HEIGHT))
        
        # バーの現在値
        fillWidth = (value / maxValue) * BAR_WIDTH
        pygame.draw.rect(screen, color,
                        (x, y, fillWidth, BAR_HEIGHT))
        
        # バーの枠
        pygame.draw.rect(screen, WHITE,
                        (x, y, BAR_WIDTH, BAR_HEIGHT), 2)
        
        # ラベル
        font = pygame.font.Font(None, 24)
        text = font.render(f"{label}: {int(value)}/{int(maxValue)}", True, WHITE)
        screen.blit(text, (x + BAR_WIDTH + 10, y))
    
    def checkCollisions(self) -> None:
        """
        衝突判定を行います。
        """
        # プレイヤーと敵の衝突判定
        for enemy in self.enemies:
            if pygame.sprite.collide_rect(self.player, enemy):
                self.player.takeDamage(enemy.damage)
        
        # 泡と敵の衝突判定
        for bubble in self.player.bubbles:
            for enemy in self.enemies:
                if pygame.sprite.collide_rect(bubble, enemy):
                    enemy.takeDamage(bubble.power)
    
    def run(self) -> None:
        """
        ゲームのメインループを実行します。
        """
        while self.isRunning:
            self.handleEvents()
            self.sceneManager.update()
            self.sceneManager.render(self.screen)
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run() 