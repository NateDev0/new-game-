#Nate 2026-01-12
import os
import sys
import pygame

# Direct paths to the specific images
MAP_PATH = r"C:\Users\NL354868689\OneDrive - District School Board of Niagara\Desktop\Lessons\personal projects\small_game\photos\photos of world\world\map.png"
PLAYER_PATH = r"C:\Users\NL354868689\OneDrive - District School Board of Niagara\Desktop\Lessons\personal projects\small_game\photos\photo of player\player.png"
HOUSE_INTERIOR_PATH = r"C:\Users\NL354868689\OneDrive - District School Board of Niagara\Desktop\Lessons\personal projects\small_game\photos\photos of inside homes\inside_trap_home1.png"
COMPUTER_PATH = r"C:\Users\NL354868689\OneDrive - District School Board of Niagara\coding\new-game-\photos\photos of world\thebeeshop.png"
# Fix item paths - adjust these to match your exact filenames
CARTS_PATH = r"C:\Users\NL354868689\OneDrive - District School Board of Niagara\Desktop\Lessons\personal projects\small_game\photos\item photos\carts.png"
FUNNEL_PATH = r"C:\Users\NL354868689\OneDrive - District School Board of Niagara\Desktop\Lessons\personal projects\small_game\photos\item photos\funnel.png"
HONEY_CURRENCY_PATH = r"C:\Users\NL354868689\OneDrive - District School Board of Niagara\coding\new-game-\photos\item photos\Honey_currency_png.png"
COIN_CURRENCY_PATH = r"C:\Users\NL354868689\OneDrive - District School Board of Niagara\coding\new-game-\photos\item photos\coin_currency.png"
THE_BEE_TREE_PATH = r"C:\Users\NL354868689\OneDrive - District School Board of Niagara\coding\new-game-\photos\item photos\the_bee_tree.png"
THE_BEE_HIVE_PATH = r"C:\Users\NL354868689\OneDrive - District School Board of Niagara\coding\new-game-\photos\item photos\The_bee_hive.png"
THE_BEE_BOX_PATH = r"C:\Users\NL354868689\OneDrive - District School Board of Niagara\coding\new-game-\photos\item photos\the_bee_box.png"
PUFFY_HONEY_PATH = r"C:\Users\NL354868689\OneDrive - District School Board of Niagara\coding\new-game-\photos\item photos\Puffy-Honey.png"
FILLUP_TABLE_PATH = r"C:\Users\NL354868689\OneDrive - District School Board of Niagara\coding\new-game-\photos\item photos\fillup_table_image.png"

# Update constants section
SCREEN_W, SCREEN_H = 800, 600
PLAYER_SPEED = 300  # pixels per second
HOTBAR_SIZE = 9
PLAYER_INVENTORY_SIZE = HOTBAR_SIZE
DRAGGING_ITEM = None
DRAG_OFFSET = (0, 0)
TUTORIAL_DONE = False  # Add this line
GROUND_ITEMS = []  # List of items dropped on ground with positions
PICKUP_RANGE = 50  # How close player needs to be to pick up items
HONEY_AMOUNT = 0  # Honey currency tracking
COIN_AMOUNT = 75  # Coin currency tracking

pygame.display.init()
pygame.font.init()
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

# Ensure player isn't enormous compared to screen: scale down if needed
def scale_surface_to_max(surf, max_size):
    w, h = surf.get_width(), surf.get_height()
    mw, mh = max_size
    if w <= mw and h <= mh:
        return surf
    scale = min(mw / w, mh / h)
    new_size = (max(1, int(w * scale)), max(1, int(h * scale)))
    return pygame.transform.smoothscale(surf, new_size)

# Load images directly from their paths
bg = pygame.image.load(MAP_PATH).convert()
player_img = pygame.image.load(PLAYER_PATH).convert_alpha()
house_interior_original = pygame.image.load(HOUSE_INTERIOR_PATH).convert()
# Scale house interior to be smaller (about 1/3 of the world size)
house_interior = scale_surface_to_max(house_interior_original, (SCREEN_W, SCREEN_H))

# Load computer image
try:
    computer_img = pygame.image.load(COMPUTER_PATH).convert_alpha()
except:
    print(f"Failed to load computer image from {COMPUTER_PATH}")
    computer_img = pygame.Surface((400, 300), pygame.SRCALPHA)
    computer_img.fill((255, 0, 0))  # Red fallback for visibility

# Scale computer image to fit screen
computer_img = scale_surface_to_max(computer_img, (SCREEN_W, SCREEN_H))

# Load FillUp Table image
try:
    fillup_table_img = pygame.image.load(FILLUP_TABLE_PATH).convert_alpha()
except:
    print(f"Failed to load FillUp Table image from {FILLUP_TABLE_PATH}")
    fillup_table_img = pygame.Surface((400, 300), pygame.SRCALPHA)
    fillup_table_img.fill((0, 255, 0))  # Green fallback for visibility

# Scale FillUp Table image to fit screen
fillup_table_img = scale_surface_to_max(fillup_table_img, (SCREEN_W, SCREEN_H))

# Load item images with fallbacks
try:
    carts_img = pygame.image.load(CARTS_PATH).convert_alpha()
except:
    print(f"Failed to load carts image from {CARTS_PATH}")
    carts_img = pygame.Surface((32, 32), pygame.SRCALPHA)
    carts_img.fill((255, 100, 100))  # Red fallback

try:
    funnel_img = pygame.image.load(FUNNEL_PATH).convert_alpha()
except:
    print(f"Failed to load funnel image from {FUNNEL_PATH}")
    funnel_img = pygame.Surface((32, 32), pygame.SRCALPHA)
    funnel_img.fill((100, 100, 255))  # Blue fallback

try:
    honey_currency_img = pygame.image.load(HONEY_CURRENCY_PATH).convert_alpha()
except:
    print(f"Failed to load honey currency image from {HONEY_CURRENCY_PATH}")
    honey_currency_img = pygame.Surface((32, 32), pygame.SRCALPHA)
    honey_currency_img.fill((255, 200, 0))  # Yellow fallback

try:
    coin_currency_img = pygame.image.load(COIN_CURRENCY_PATH).convert_alpha()
except:
    print(f"Failed to load coin currency image from {COIN_CURRENCY_PATH}")
    coin_currency_img = pygame.Surface((32, 32), pygame.SRCALPHA)
    coin_currency_img.fill((200, 200, 100))  # Silver fallback

try:
    the_bee_tree_img = pygame.image.load(THE_BEE_TREE_PATH).convert_alpha()
except:
    print(f"Failed to load bee tree image from {THE_BEE_TREE_PATH}")
    the_bee_tree_img = pygame.Surface((32, 32), pygame.SRCALPHA)
    the_bee_tree_img.fill((100, 200, 50))  # Green fallback

try:
    the_bee_hive_img = pygame.image.load(THE_BEE_HIVE_PATH).convert_alpha()
except:
    print(f"Failed to load bee hive image from {THE_BEE_HIVE_PATH}")
    the_bee_hive_img = pygame.Surface((32, 32), pygame.SRCALPHA)
    the_bee_hive_img.fill((200, 100, 50))  # Brown fallback

try:
    the_bee_box_img = pygame.image.load(THE_BEE_BOX_PATH).convert_alpha()
except:
    print(f"Failed to load bee box image from {THE_BEE_BOX_PATH}")
    the_bee_box_img = pygame.Surface((32, 32), pygame.SRCALPHA)
    the_bee_box_img.fill((150, 100, 75))  # Tan fallback

try:
    puffy_honey_img = pygame.image.load(PUFFY_HONEY_PATH).convert_alpha()
except:
    print(f"Failed to load puffy honey image from {PUFFY_HONEY_PATH}")
    puffy_honey_img = pygame.Surface((32, 32), pygame.SRCALPHA)
    puffy_honey_img.fill((255, 200, 100))  # Orange fallback

# World sizes - calculate these FIRST after loading images
WORLD_W, WORLD_H = bg.get_width(), bg.get_height()
HOUSE_W, HOUSE_H = house_interior.get_width(), house_interior.get_height()

# Scale player bigger so it's more visible
player_img = scale_surface_to_max(player_img, (256,256))

# If the player image is still the same visual as the background (e.g. it's huge),
# create a tiny visible fallback so you can move something.
if player_img.get_width() > WORLD_W // 2 or player_img.get_height() > WORLD_H // 2:
    print("Player image looks very large compared to the map; using fallback small sprite instead.")
    player_img = pygame.Surface((32, 32), pygame.SRCALPHA)
    player_img.fill((200, 50, 50))

# Give the window a title so it's obvious you're running the map/player demo
pygame.display.set_caption("Map - Move the player with Arrow keys / WASD")

# Player setup (world coords) - start centered on the map
# Player setup (world coords) - start centered on the map
# Use smaller hitbox size instead of full image size
PLAYER_HITBOX_SIZE = 164
player = pygame.Rect(0, 0, PLAYER_HITBOX_SIZE, PLAYER_HITBOX_SIZE)
player.x = max(0, min(WORLD_W - player.width, WORLD_W // 2 - player.width // 2))
player.y = max(0, min(WORLD_H - player.height, WORLD_H // 2 - player.height // 2))

def clamp(value, a, b):
    return max(a, min(b, value))

CENTER_CAMERA = True  # Changed from False to True - enable camera following by default

def get_camera_offset(player_rect):
    # Center camera on player but clamp to world bounds
    x = player_rect.centerx - SCREEN_W // 2
    y = player_rect.centery - SCREEN_H // 2
    
    # Ensure we don't show beyond map edges
    x = clamp(x, 0, max(0, WORLD_W - SCREEN_W))
    y = clamp(y, 0, max(0, WORLD_H - SCREEN_H))
    return x, y

def draw_text(surf, text, x, y, color=(255, 255, 255)):
    img = font.render(text, True, color)
    surf.blit(img, (x, y))

def draw_centered_popup(surf, text, color=(255, 255, 0)):
    # Create semi-transparent background
    overlay = pygame.Surface((SCREEN_W, 80), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))  # Black with 180 alpha (semi-transparent)
    
    # Draw the background centered vertically
    y_pos = SCREEN_H // 2 - 40  # 40 is half the overlay height
    surf.blit(overlay, (0, y_pos))
    
    # Draw text centered
    text_img = font.render(text, True, color)
    x_pos = SCREEN_W // 2 - text_img.get_width() // 2
    y_pos = SCREEN_H // 2 - text_img.get_height() // 2
    surf.blit(text_img, (x_pos, y_pos))

# House entrance zone at (0,0)
HOUSE_ENTRANCE = pygame.Rect(0, 0, 100, 100)  # Interaction zone size
SHELF_LOCATION = pygame.Rect(496, 156, 40, 40)  # Smaller hitbox centered at shelf location

# Computer interaction
COMPUTER_LOCATION = pygame.Rect(0, 0, 50, 50)  # Area from (0,0) to (49,49) approx
COMPUTER_OPEN = False  # Track if computer interface is open

# Computer shop button definitions
# (x1, y1, x2, y2) - top-left to bottom-right
BEE_TREE_BUTTON = pygame.Rect(64, 242, 196 - 64, 264 - 242)

# FillUp Table interaction
FILLUP_TABLE_LOCATION = pygame.Rect(96, 0, 195, 1)  # x=104 to 195, y=0 inside trap house
FILLUP_TABLE_OPEN = False  # Track if FillUp Table interface is open

# Shelf interaction variables
SHELF_INVENTORY_SIZE = 20
SHELF_OPEN = False  # Track if shelf interface is open

# Update shelf items with proper names
shelf_items = [
    {"name": "Empty Honey Cartridge", "quantity": 1, "image": carts_img},
    {"name": "Funnel", "quantity": 1, "image": funnel_img}
]

# Replace player_inventory initialization
player_inventory = [None] * HOTBAR_SIZE  # Initialize with empty slots

def draw_inventory_interface(surf, items, start_x, start_y, max_slots, title=None, hover_idx=None, hover_scroll=0):
    if title:
        draw_text(surf, title, start_x, start_y - 30, (255, 255, 255))
    
    slot_size = 40
    slots_per_row = 5
    
    for i in range(max_slots):
        x = start_x + (i % slots_per_row) * (slot_size + 10)
        y = start_y + (i // slots_per_row) * (slot_size + 10)
        
        # Draw slot background
        pygame.draw.rect(surf, (100, 100, 100), (x, y, slot_size, slot_size))
        
        # Draw item if exists and is not None
        if i < len(items) and items[i] is not None:
            item = items[i]
            # Scale and draw item image
            scaled_img = scale_surface_to_max(item["image"], (slot_size-4, slot_size-4))
            img_x = x + (slot_size - scaled_img.get_width()) // 2
            img_y = y + (slot_size - scaled_img.get_height()) // 2
            surf.blit(scaled_img, (img_x, img_y))

            # Draw quantity
            draw_text(surf, str(item["quantity"]), x + slot_size - 20, y + slot_size - 20, (255, 255, 0))
            
            # Draw item name inside slot at bottom, with clipping and hover slide
            name_y = y + slot_size - 15
            text_surf = font.render(item["name"], True, (200, 200, 200))
            text_width = text_surf.get_width()
            if i == hover_idx and text_width > slot_size:
                surf.blit(text_surf, (x - hover_scroll, name_y))
            else:
                if text_width > slot_size:
                    clipped_surf = text_surf.subsurface((0, 0, slot_size, text_surf.get_height()))
                    surf.blit(clipped_surf, (x, name_y))
                else:
                    surf.blit(text_surf, (x, name_y))

def draw_shelf_interface(surf, hover_idx=None, hover_scroll=0):
    # Draw semi-transparent full-screen overlay
    overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    surf.blit(overlay, (0, 0))
    
    # Draw only shelf inventory (removed player inventory section)
    draw_inventory_interface(surf, shelf_items, SCREEN_W//4, SCREEN_H//4, SHELF_INVENTORY_SIZE, "Shelf Items", hover_idx, hover_scroll)

def draw_fillup_table_interface(surf):
    # Scale image to fill the entire screen
    scaled_img = pygame.transform.scale(fillup_table_img, (SCREEN_W, SCREEN_H))
    surf.blit(scaled_img, (0, 0))
    
    # Draw honey counter overlay at top right
    scaled_honey_img = scale_surface_to_max(honey_currency_img, (48, 48))
    surf.blit(scaled_honey_img, (SCREEN_W - 200, 10))
    
    # Draw honey text with black outline
    honey_text_img = font.render(f"Honey: {HONEY_AMOUNT}", True, (255, 255, 0))
    honey_outline_text = font.render(f"Honey: {HONEY_AMOUNT}", True, (0, 0, 0))
    
    # Draw black outline (offset in 8 directions)
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx != 0 or dy != 0:
                surf.blit(honey_outline_text, (SCREEN_W - 140 + dx, 25 + dy))
    
    # Draw yellow text on top
    surf.blit(honey_text_img, (SCREEN_W - 140, 25))
    
    # Draw ESC instruction in top left corner in yellow with black outline
    text_img = font.render("Press ESC to go back", True, (255, 255, 0))
    outline_text = font.render("Press ESC to go back", True, (0, 0, 0))
    
    # Draw black outline (offset in 8 directions)
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx != 0 or dy != 0:
                surf.blit(outline_text, (10 + dx, 10 + dy))
    
    # Draw yellow text on top
    surf.blit(text_img, (10, 10))
    
    # Optional: Show mouse coordinates to help you plot clickable areas
    mouse_pos = pygame.mouse.get_pos()
    draw_text(surf, f"Mouse: {mouse_pos[0]},{mouse_pos[1]}", 10, 30, (0, 255, 0))

def draw_hotbar(surf):
    slot_size = 40
    margin = 4
    total_width = (slot_size + margin) * HOTBAR_SIZE - margin
    start_x = SCREEN_W // 2 - total_width // 2
    start_y = SCREEN_H - slot_size - 10
    
    # Draw background
    bar_bg = pygame.Surface((total_width + 8, slot_size + 8), pygame.SRCALPHA)
    bar_bg.fill((0, 0, 0, 180))
    surf.blit(bar_bg, (start_x - 4, start_y - 4))
    
    # Draw slots
    for i in range(HOTBAR_SIZE):
        x = start_x + i * (slot_size + margin)
        # Draw slot background
        pygame.draw.rect(surf, (100, 100, 100), (x, start_y, slot_size, slot_size))
        
        # Draw item if exists
        if player_inventory[i]:
            item = player_inventory[i]
            scaled_img = scale_surface_to_max(item["image"], (slot_size-4, slot_size-4))
            img_x = x + (slot_size - scaled_img.get_width()) // 2
            img_y = start_y + (slot_size - scaled_img.get_height()) // 2
            surf.blit(scaled_img, (img_x, img_y))
            if item["quantity"] > 1:
                draw_text(surf, str(item["quantity"]), x + slot_size - 20, start_y + slot_size - 20, (255, 255, 0))

def draw_dragged_item(surf, item, pos):
    if not item:
        return
    scaled_img = scale_surface_to_max(item["image"], (40, 40))
    surf.blit(scaled_img, (pos[0] - scaled_img.get_width()//2, pos[1] - scaled_img.get_height()//2))
    if item["quantity"] > 1:
        draw_text(surf, str(item["quantity"]), pos[0] + 10, pos[1] + 10, (255, 255, 0))

def get_hotbar_slot_at(pos):
    slot_size = 40
    margin = 4
    total_width = (slot_size + margin) * HOTBAR_SIZE - margin
    start_x = SCREEN_W // 2 - total_width // 2
    start_y = SCREEN_H - slot_size - 10
    
    if start_y <= pos[1] <= start_y + slot_size:
        slot_x = (pos[0] - start_x) // (slot_size + margin)
        if 0 <= slot_x < HOTBAR_SIZE:
            return slot_x
    return None

def handle_inventory_click(pos, items, max_slots, start_x, start_y):
    slot_size = 40
    slots_per_row = 5
    
    for i in range(min(len(items), max_slots)):
        x = start_x + (i % slots_per_row) * (slot_size + 10)
        y = start_y + (i // slots_per_row) * (slot_size + 10)
        
        if x <= pos[0] <= x + slot_size and y <= pos[1] <= y + slot_size:
            return i
    return None

def transfer_item(from_inv, to_inv, item_idx, max_slots):
    if item_idx >= len(from_inv) or len(to_inv) >= max_slots:
        return
    
    item = from_inv[item_idx]
    to_inv.append(item)
    from_inv.pop(item_idx)

class PlantedItem:
    def __init__(self, item_type, item_dict, x, y, honey_per_second):
        self.item_type = item_type  # "bee_tree", "bee_hive", "bee_box"
        self.item = item_dict  # The item dictionary with image, name, quantity
        self.x = x
        self.y = y
        self.honey_per_second = honey_per_second
        self.rect = pygame.Rect(x, y, 32, 32)

class GroundItem:
    def __init__(self, item_dict, x, y):
        # item_dict expected to be a dict with keys: 'name', 'quantity', 'image'
        self.item = item_dict
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 32, 32)

# Define planting zones at specific Y coordinates
PLANTING_ZONES = [
    pygame.Rect(0, 80, 50, 10),    # Y=85
    pygame.Rect(0, 155, 50, 10),   # Y=160
    pygame.Rect(0, 219, 50, 10),   # Y=224
    pygame.Rect(0, 307, 50, 10)    # Y=312
]

# List to store planted items
PLANTED_ITEMS = []

# Honey production accumulator
HONEY_PRODUCTION_TIMER = 0.0

# Add before main()
def get_item_drop_position(player_rect):
    # Drop item slightly in front of player
    return (player_rect.centerx, player_rect.centery + 40)

def draw_ground_items(surf, cam_x, cam_y):
    for ground_item in GROUND_ITEMS:
        # Draw item image
        item_name = ground_item.item["name"]
        if item_name in ["The Bee Box", "The Bee Hive", "The Bee Tree"]:
            scaled_img = scale_surface_to_max(ground_item.item["image"], (64, 64))
        else:
            scaled_img = scale_surface_to_max(ground_item.item["image"], (32, 32))
        screen_x = ground_item.x - cam_x - scaled_img.get_width()//2
        screen_y = ground_item.y - cam_y - scaled_img.get_height()//2
        surf.blit(scaled_img, (screen_x, screen_y))

def draw_planted_items(surf, cam_x, cam_y):
    for planted_item in PLANTED_ITEMS:
        # Draw planted item image
        scaled_img = scale_surface_to_max(planted_item.item["image"], (32, 32))
        screen_x = planted_item.x - cam_x - scaled_img.get_width()//2
        screen_y = planted_item.y - cam_y - scaled_img.get_height()//2
        surf.blit(scaled_img, (screen_x, screen_y))

def draw_computer_interface(surf):
    # Scale image to fill the entire screen
    scaled_img = pygame.transform.scale(computer_img, (SCREEN_W, SCREEN_H))
    surf.blit(scaled_img, (0, 0))
    
    # Draw honey currency display at bottom left with larger size and outline
    scaled_honey_img = scale_surface_to_max(honey_currency_img, (64, 64))
    surf.blit(scaled_honey_img, (350, 530))
    
    # Draw honey text with black outline
    honey_text_img = font.render(f"Honey: {HONEY_AMOUNT}", True, (255, 255, 0))
    honey_outline_text = font.render(f"Honey: {HONEY_AMOUNT}", True, (0, 0, 0))
    
    # Draw black outline (offset in 8 directions)
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx != 0 or dy != 0:
                surf.blit(honey_outline_text, (425 + dx, 555 + dy))
    
    # Draw yellow text on top
    surf.blit(honey_text_img, (425, 555))
    
    # Draw coin currency display at bottom right with larger size and outline
    scaled_coin_img = scale_surface_to_max(coin_currency_img, (64, 64))
    surf.blit(scaled_coin_img, (580, 530))
    
    # Draw coin text with black outline
    coin_text_img = font.render(f"Coins($): {COIN_AMOUNT}", True, (200, 200, 100))
    coin_outline_text = font.render(f"Coins($): {COIN_AMOUNT}", True, (0, 0, 0))
    
    # Draw black outline (offset in 8 directions)
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx != 0 or dy != 0:
                surf.blit(coin_outline_text, (655 + dx, 555 + dy))
    
    # Draw silver text on top
    surf.blit(coin_text_img, (655, 555))
    
    # Draw ESC instruction in top left corner in yellow with black outline
    text_img = font.render("Press ESC to go back", True, (255, 255, 0))
    outline_text = font.render("Press ESC to go back", True, (0, 0, 0))
    
    # Draw black outline (offset in 8 directions)
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx != 0 or dy != 0:
                surf.blit(outline_text, (10 + dx, 10 + dy))
    
    # Draw yellow text on top
    surf.blit(text_img, (10, 10))

def find_closest_item(player_rect):
    for ground_item in GROUND_ITEMS:
        # Convert ground item position to be relative to player's world position
        dist_x = abs(player_rect.centerx - ground_item.x)
        dist_y = abs(player_rect.centery - ground_item.y)
        if dist_x < PICKUP_RANGE and dist_y < PICKUP_RANGE:
            return ground_item
    return None

def find_closest_planted_item(player_rect):
    for planted_item in PLANTED_ITEMS:
        # Check if player is close enough to planted item
        dist_x = abs(player_rect.centerx - planted_item.x)
        dist_y = abs(player_rect.centery - planted_item.y)
        if dist_x < PICKUP_RANGE and dist_y < PICKUP_RANGE:
            return planted_item
    return None

def draw_honey_display(surf):
    # Scale honey currency image to small size
    scaled_img = scale_surface_to_max(honey_currency_img, (32, 32))
    # Draw image
    surf.blit(scaled_img, (10, 70))
    # Draw honey amount text next to image
    draw_text(surf, f"Honey: {HONEY_AMOUNT}", 50, 75, (255, 255, 0))

def draw_coin_display(surf):
    # Scale coin currency image to small size
    scaled_img = scale_surface_to_max(coin_currency_img, (32, 32))
    # Draw image
    surf.blit(scaled_img, (10, 105))
    # Draw coin amount text next to image
    draw_text(surf, f"Coins($): {COIN_AMOUNT}", 50, 110, (200, 200, 100))

def main():
    running = True
    inside_house = False
    global SHELF_OPEN, DRAGGING_ITEM, TUTORIAL_DONE, COMPUTER_OPEN, HONEY_AMOUNT, COIN_AMOUNT, HONEY_PRODUCTION_TIMER, FILLUP_TABLE_OPEN
    
    # Store where player was before entering house
    pre_house_position = None

    # Hover variables for shelf text sliding
    hover_idx = None
    hover_scroll = 0.0

    while running:
        dt = clock.tick(60) / 1000.0  # seconds
        mouse_pos = pygame.mouse.get_pos()

        # Compute camera offset early so we can convert mouse->world coords inside event handling
        if inside_house:
            x = player.centerx - SCREEN_W // 2
            y = player.centery - SCREEN_H // 2
            cam_x = clamp(x, 0, max(0, HOUSE_W - SCREEN_W))
            cam_y = clamp(y, 0, max(0, HOUSE_H - SCREEN_H))
        else:
            cam_x, cam_y = get_camera_offset(player)

        # Update hover for shelf text sliding
        if SHELF_OPEN:
            idx = handle_inventory_click(mouse_pos, shelf_items, SHELF_INVENTORY_SIZE, SCREEN_W//4, SCREEN_H//4)
            if idx is not None and idx < len(shelf_items):
                if idx == hover_idx:
                    item = shelf_items[idx]
                    text_width = font.size(item["name"])[0]
                    if text_width > 40:
                        hover_scroll = min(hover_scroll + dt * 100, text_width - 40)
                else:
                    hover_idx = idx
                    hover_scroll = 0.0
            else:
                hover_idx = None
                hover_scroll = 0.0
        else:
            hover_idx = None
            hover_scroll = 0.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    # Try to pick up planted item first
                    closest_planted = find_closest_planted_item(player)
                    if closest_planted:
                        # Add item back to inventory
                        for i in range(HOTBAR_SIZE):
                            if player_inventory[i] is None:
                                player_inventory[i] = closest_planted.item.copy()
                                PLANTED_ITEMS.remove(closest_planted)
                                break
                        continue
                    
                    # Try to pick up item if we're near one and not in a menu
                    if not SHELF_OPEN:
                        closest_item = find_closest_item(player)
                        if closest_item:
                            # Find empty hotbar slot
                            for i in range(HOTBAR_SIZE):
                                if player_inventory[i] is None:
                                    player_inventory[i] = closest_item.item
                                    GROUND_ITEMS.remove(closest_item)
                                    break
                            continue  # Skip other E key handling if we picked up an item

                    # Original E key handling for shelf/house
                    if SHELF_OPEN:
                        SHELF_OPEN = False
                    elif COMPUTER_OPEN:
                        COMPUTER_OPEN = False
                    elif FILLUP_TABLE_OPEN:
                        FILLUP_TABLE_OPEN = False
                    elif inside_house:
                        # Check if player is close enough to FillUp Table first
                        if FILLUP_TABLE_LOCATION.colliderect(player):
                            FILLUP_TABLE_OPEN = True
                        # Check if player is close enough to computer
                        elif COMPUTER_LOCATION.colliderect(player):
                            COMPUTER_OPEN = True
                        else:
                            # Check if player is close enough to shelf (using center points)
                            player_center_x = player.centerx
                            player_center_y = player.centery
                            shelf_center_x = SHELF_LOCATION.centerx
                            shelf_center_y = SHELF_LOCATION.centery
                            
                            distance = ((player_center_x - shelf_center_x)**2 + (player_center_y - shelf_center_y)**2)**0.5
                            
                            if distance < 100:  # Increased from 10 to 100 for easier interaction
                                SHELF_OPEN = True
                    elif not inside_house:
                        # Existing house entrance logic
                        if HOUSE_ENTRANCE.colliderect(player):
                            # Save current position before entering
                            pre_house_position = (player.x, player.y)
                            inside_house = True
                            # Place player at bottom middle of house interior
                            player.x = HOUSE_W // 2 - player.width // 2
                            player.y = HOUSE_H - player.height - 50
                
                elif event.key == pygame.K_ESCAPE:
                    if COMPUTER_OPEN:
                        COMPUTER_OPEN = False
                    elif SHELF_OPEN:
                        SHELF_OPEN = False
                    elif FILLUP_TABLE_OPEN:
                        FILLUP_TABLE_OPEN = False
                    elif inside_house:
                        # Exit house
                        inside_house = False
                        # Return to saved position or default to just outside entrance
                        if pre_house_position:
                            player.x, player.y = pre_house_position
                        else:
                            player.x = HOUSE_ENTRANCE.x + HOUSE_ENTRANCE.width
                            player.y = HOUSE_ENTRANCE.y + HOUSE_ENTRANCE.height
                    else:
                        # Only quit game if outside
                        running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    mods = pygame.key.get_mods()
                    is_shift = mods & pygame.KMOD_SHIFT
                    
                    # Check computer shop button clicks
                    if COMPUTER_OPEN:
                        if BEE_TREE_BUTTON.collidepoint(mouse_pos):
                            # Purchase The Bee Tree for 25 coins
                            if COIN_AMOUNT >= 25:
                                COIN_AMOUNT -= 25
                                # Add item to inventory
                                for i in range(HOTBAR_SIZE):
                                    if player_inventory[i] is None:
                                        player_inventory[i] = {"name": "The Bee Tree", "quantity": 1, "image": the_bee_tree_img}
                                        break
                    
                    if SHELF_OPEN:
                        # Handle shelf inventory clicks
                        idx = handle_inventory_click(mouse_pos, shelf_items, SHELF_INVENTORY_SIZE, 
                                                  SCREEN_W//4, SCREEN_H//4)
                        if idx is not None and idx < len(shelf_items):
                            if is_shift:
                                # Quick move to hotbar
                                for i in range(HOTBAR_SIZE):
                                    if player_inventory[i] is None:
                                        player_inventory[i] = shelf_items.pop(idx)
                                        break
                            else:
                                DRAGGING_ITEM = shelf_items.pop(idx)
                    
                    # Handle hotbar clicks
                    slot = get_hotbar_slot_at(mouse_pos)
                    if slot is not None:
                        if is_shift:
                            # Quick move to shelf, or drop on ground if shelf is full
                            if player_inventory[slot] is not None:
                                if len(shelf_items) < SHELF_INVENTORY_SIZE:
                                    shelf_items.append(player_inventory[slot])
                                    player_inventory[slot] = None
                                else:
                                    # Shelf is full, drop item on ground instead
                                    drop_x, drop_y = get_item_drop_position(player)
                                    GROUND_ITEMS.append(GroundItem(player_inventory[slot], drop_x, drop_y))
                                    player_inventory[slot] = None
                        elif DRAGGING_ITEM:
                            # Swap items
                            temp = player_inventory[slot]
                            player_inventory[slot] = DRAGGING_ITEM
                            DRAGGING_ITEM = temp
                        elif player_inventory[slot]:
                            DRAGGING_ITEM = player_inventory[slot]
                            player_inventory[slot] = None
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and DRAGGING_ITEM:  # Left click release
                    slot = get_hotbar_slot_at(mouse_pos)
                    if slot is not None:
                        # If dropping on hotbar slot
                        temp = player_inventory[slot]
                        player_inventory[slot] = DRAGGING_ITEM
                        DRAGGING_ITEM = temp
                        TUTORIAL_DONE = True
                    elif SHELF_OPEN:
                        # If over shelf area, return to shelf
                        shelf_area = pygame.Rect(SCREEN_W//4, SCREEN_H//4, 
                                          SHELF_INVENTORY_SIZE * 50, 200)
                        if shelf_area.collidepoint(mouse_pos):
                            shelf_items.append(DRAGGING_ITEM)
                            DRAGGING_ITEM = None
                            TUTORIAL_DONE = True
                    else:
                        # Check if dropping in a planting zone (when inside house)
                        item_planted = False
                        if inside_house:
                            for zone in PLANTING_ZONES:
                                # Convert mouse screen position to world coordinates
                                mouse_world_x = mouse_pos[0] + cam_x
                                mouse_world_y = mouse_pos[1] + cam_y
                                if zone.collidepoint(mouse_world_x, mouse_world_y):
                                    # Plant the item
                                    item_type = None
                                    honey_rate = 0
                                    if DRAGGING_ITEM["name"] == "The Bee Tree":
                                        item_type = "bee_tree"
                                        honey_rate = 1
                                    elif DRAGGING_ITEM["name"] == "The Bee Hive":
                                        item_type = "bee_hive"
                                        honey_rate = 100
                                    elif DRAGGING_ITEM["name"] == "The Bee Box":
                                        item_type = "bee_box"
                                        honey_rate = 4

                                    if item_type:
                                        # Place planted item centered in the planting zone
                                        planted_x = zone.centerx
                                        planted_y = zone.centery
                                        planted = PlantedItem(item_type, DRAGGING_ITEM.copy(), planted_x, planted_y, honey_rate)
                                        PLANTED_ITEMS.append(planted)
                                        DRAGGING_ITEM = None
                                        item_planted = True
                                        break
                        
                        # If not planted, drop item on ground
                        if not item_planted:
                            drop_x, drop_y = get_item_drop_position(player)
                            GROUND_ITEMS.append(GroundItem(DRAGGING_ITEM, drop_x, drop_y))
                            DRAGGING_ITEM = None

        # Input
        keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += 1

        # Normalize diagonal movement
        if dx != 0 and dy != 0:
            inv = 1 / (2 ** 0.5)
            dx *= inv
            dy *= inv

        player.x += int(dx * PLAYER_SPEED * dt)
        player.y += int(dy * PLAYER_SPEED * dt)
        
        # Update honey production from planted items
        HONEY_PRODUCTION_TIMER += dt
        if HONEY_PRODUCTION_TIMER >= 1.0:  # Produce honey every second
            for planted_item in PLANTED_ITEMS:
                HONEY_AMOUNT += planted_item.honey_per_second
            # Also produce honey from ground items (Bee Tree, Bee Hive, Bee Box)
            for ground_item in GROUND_ITEMS:
                if ground_item.item["name"] == "The Bee Tree":
                    HONEY_AMOUNT += 1
                elif ground_item.item["name"] == "The Bee Hive":
                    HONEY_AMOUNT += 100
                elif ground_item.item["name"] == "The Bee Box":
                    HONEY_AMOUNT += 4
            HONEY_PRODUCTION_TIMER = 0.0

        # Clamp player to current world boundaries (house or outside)
        if inside_house:
            player.x = clamp(player.x, 0, HOUSE_W - player.width)
            player.y = clamp(player.y, 0, HOUSE_H - player.height)
        else:
            player.x = clamp(player.x, 0, WORLD_W - player.width)
            player.y = clamp(player.y, 0, WORLD_H - player.height)

        # Camera offset - use house dimensions when inside
        if inside_house:
            x = player.centerx - SCREEN_W // 2
            y = player.centery - SCREEN_H // 2
            cam_x = clamp(x, 0, max(0, HOUSE_W - SCREEN_W))
            cam_y = clamp(y, 0, max(0, HOUSE_H - SCREEN_H))
        else:
            cam_x, cam_y = get_camera_offset(player)

        # Draw current scene
        screen.fill((0, 0, 0))
        
        # Only draw game if computer or fillup table is not open
        if not COMPUTER_OPEN and not FILLUP_TABLE_OPEN:
            if inside_house:
                screen.blit(house_interior, (-cam_x, -cam_y))
            else:
                screen.blit(bg, (-cam_x, -cam_y))
            
            # Draw ground items before player
            draw_ground_items(screen, cam_x, cam_y)
            # Draw planted items
            if inside_house:
                draw_planted_items(screen, cam_x, cam_y)
            screen.blit(player_img, (player.x - cam_x, player.y - cam_y))

        # UI
        draw_text(screen, "Move: Arrow keys / WASD   Enter/Exit: E/ESC   Quit: Close", 10, 10)
        if inside_house:
            # Calculate distance to shelf for interaction prompt
            player_center_x = player.centerx
            player_center_y = player.centery
            shelf_center_x = SHELF_LOCATION.centerx
            shelf_center_y = SHELF_LOCATION.centery
            distance = ((player_center_x - shelf_center_x)**2 + (player_center_y - shelf_center_y)**2)**0.5
            
            # Show shelf interaction prompt when near
            if distance < 100 and not SHELF_OPEN:
                draw_centered_popup(screen, "Press E to open shelf")
            
            # Show computer interaction prompt when near inside house
            if COMPUTER_LOCATION.colliderect(player) and not COMPUTER_OPEN:
                draw_centered_popup(screen, "Press E to open computer")
            
            # Show FillUp Table interaction prompt when near inside house
            if FILLUP_TABLE_LOCATION.colliderect(player) and not FILLUP_TABLE_OPEN:
                draw_centered_popup(screen, "Press E to open FillUp Table")
            
            # Draw exit instruction
            draw_text(screen, "Press ESC to leave house", SCREEN_W - 200, 10, color=(255, 255, 0))
            
            # Draw shelf inventory if open
            if SHELF_OPEN:
                draw_shelf_interface(screen, hover_idx, hover_scroll)
        
        elif HOUSE_ENTRANCE.colliderect(player):
            # Show enter house popup only when outside near entrance
            draw_centered_popup(screen, "Press E to enter house")
        
        # Debug: show player world coordinates and FPS
        if not COMPUTER_OPEN and not FILLUP_TABLE_OPEN:
            draw_text(screen, f"Player: {player.x},{player.y}  FPS: {int(clock.get_fps())}", 10, 30)
            # Add this new line to show mouse world position when inside house
            if inside_house:
                mouse_world_x = mouse_pos[0] + cam_x
                mouse_world_y = mouse_pos[1] + cam_y
                draw_text(screen, f"Mouse World: {mouse_world_x},{mouse_world_y}", 10, 50, (0, 255, 0))
            # Draw honey currency display
            draw_honey_display(screen)
            # Draw coin currency display
            draw_coin_display(screen)
        # Draw hotbar
        draw_hotbar(screen)
        
        # Draw computer interface if open
        if COMPUTER_OPEN:
            draw_computer_interface(screen)
        
        # Draw FillUp Table interface if open
        if FILLUP_TABLE_OPEN:
            draw_fillup_table_interface(screen)
        
        # Draw dragged item last so it's on top
        if DRAGGING_ITEM:
            draw_dragged_item(screen, DRAGGING_ITEM, mouse_pos)

        # Show pickup prompt if near item
        closest_item = find_closest_item(player)
        if closest_item:
            draw_centered_popup(screen, f"{closest_item.item['name']} - Press E to pick up")
        
        # Show pickup prompt if near planted item
        closest_planted = find_closest_planted_item(player)
        if closest_planted:
            draw_centered_popup(screen, f"Press E to pick up {closest_planted.item['name']}")

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()