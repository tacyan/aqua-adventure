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
import os
from typing import Dict, List, Tuple, Optional
from src.game.player import Player
from src.game.enemy import Enemy, Jellyfish

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
        
        # ゲーム状態の初期化
        self.gameState = "TITLE"  # TITLE, PLAYING, PAUSED, GAME_OVER
        
        # ゲームオブジェクトの初期化
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.enemies: List[Enemy] = []
        
        # 敵の生成
        self.enemies.append(Jellyfish(100, 100))
        self.enemies.append(Jellyfish(700, 100))
    
    def handleEvents(self) -> None:
        """
        Pygameのイベントを処理します。
        キー入力、ウィンドウクローズなどのイベントを処理します。
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.isRunning = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.gameState == "PLAYING":
                        self.gameState = "PAUSED"
                    elif self.gameState == "PAUSED":
                        self.gameState = "PLAYING"
                elif event.key == pygame.K_SPACE and self.gameState == "TITLE":
                    self.gameState = "PLAYING"
                elif event.key == pygame.K_q and self.gameState == "PAUSED":
                    self.isRunning = False
    
    def update(self) -> None:
        """
        ゲームの状態を更新します。
        現在のゲーム状態に応じて、適切な更新処理を実行します。
        """
        if self.gameState == "PLAYING":
            # プレイヤーの更新
            self.player.update()
            
            # 敵の更新
            for enemy in self.enemies:
                enemy.update(self.player.position)
            
            # 泡と敵の衝突判定
            for bubble in self.player.bubbles:
                for enemy in self.enemies:
                    if enemy.isAlive and bubble.rect.colliderect(enemy.rect):
                        enemy.takeDamage(self.player.power)
                        bubble.hit()
            
            # プレイヤーと敵の衝突判定
            for enemy in self.enemies:
                if enemy.isAlive and self.player.rect.colliderect(enemy.rect):
                    self.player.takeDamage(enemy.damage)
            
            # 死亡した敵の削除
            self.enemies = [enemy for enemy in self.enemies if enemy.isAlive]
    
    def render(self) -> None:
        """
        ゲーム画面を描画します。
        現在のゲーム状態に応じて、適切な描画処理を実行します。
        """
        self.screen.fill(BLUE)  # 背景を青色で塗りつぶし（水中表現）
        
        if self.gameState == "PLAYING":
            # プレイヤーの描画
            self.screen.blit(self.player.image, self.player.rect)
            
            # 泡の描画
            for bubble in self.player.bubbles:
                self.screen.blit(bubble.image, bubble.rect)
            
            # 敵の描画
            for enemy in self.enemies:
                self.screen.blit(enemy.image, enemy.rect)
            
            # ステータスバーの描画
            self.renderStatusBars()
        elif self.gameState == "TITLE":
            self.renderTitle()
        elif self.gameState == "PAUSED":
            # ゲーム画面を暗く表示
            self.renderPause()
        
        pygame.display.flip()
    
    def renderStatusBars(self) -> None:
        """
        プレイヤーのステータスバーを描画します。
        """
        # HPバー
        hp_ratio = self.player.hp / self.player.maxHp
        pygame.draw.rect(self.screen, (255, 0, 0), (10, 10, 200, 20))
        pygame.draw.rect(self.screen, (0, 255, 0), (10, 10, 200 * hp_ratio, 20))
        
        # スタミナバー
        stamina_ratio = self.player.stamina / self.player.maxStamina
        pygame.draw.rect(self.screen, (128, 128, 128), (10, 40, 200, 20))
        pygame.draw.rect(self.screen, (255, 255, 0), (10, 40, 200 * stamina_ratio, 20))
        
        # 酸素バー
        oxygen_ratio = self.player.oxygen / self.player.maxOxygen
        pygame.draw.rect(self.screen, (0, 0, 128), (10, 70, 200, 20))
        pygame.draw.rect(self.screen, (0, 191, 255), (10, 70, 200 * oxygen_ratio, 20))
    
    def renderTitle(self) -> None:
        """
        タイトル画面を描画します。
        """
        font = pygame.font.Font(None, 74)
        title = font.render("アクアアドベンチャー", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/3))
        self.screen.blit(title, title_rect)
        
        font = pygame.font.Font(None, 36)
        start = font.render("Press SPACE to Start", True, WHITE)
        start_rect = start.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT*2/3))
        self.screen.blit(start, start_rect)
    
    def renderPause(self) -> None:
        """
        ポーズ画面を描画します。
        """
        font = pygame.font.Font(None, 74)
        pause = font.render("PAUSE", True, WHITE)
        pause_rect = pause.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        self.screen.blit(pause, pause_rect)
    
    def run(self) -> None:
        """
        ゲームのメインループを実行します。
        """
        while self.isRunning:
            self.handleEvents()
            self.update()
            self.render()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
