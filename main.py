import os
import sys
import pygame

# Direct paths to the specific images
MAP_PATH = r"C:\Users\NL354868689\OneDrive - District School Board of Niagara\Desktop\Lessons\personal projects\small_game\photos\photos of world\world\map.png"
PLAYER_PATH = r"C:\Users\NL354868689\OneDrive - District School Board of Niagara\Desktop\Lessons\personal projects\small_game\photos\photo of player\player.png"
HOUSE_INTERIOR_PATH = r"C:\Users\NL354868689\OneDrive - District School Board of Niagara\Desktop\Lessons\personal projects\small_game\photos\photos of inside homes\inside_trap_home1.png"
# Fix item paths - adjust these to match your exact filenames
CARTS_PATH = r"C:\Users\NL354868689\OneDrive - District School Board of Niagara\Desktop\Lessons\personal projects\small_game\photos\item photos\carts.png"
FUNNEL_PATH = r"C:\Users\NL354868689\OneDrive - District School Board of Niagara\Desktop\Lessons\personal projects\small_game\photos\item photos\funnel.png"

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

pygame.init()
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

# World sizes - calculate these FIRST after loading images
WORLD_W, WORLD_H = bg.get_width(), bg.get_height()
HOUSE_W, HOUSE_H = house_interior.get_width(), house_interior.get_height()

# Scale player bigger so it's more visible
player_img = scale_surface_to_max(player_img, (256, 256))  # Increased from 128 to 256

# If the player image is still the same visual as the background (e.g. it's huge),
# create a tiny visible fallback so you can move something.
if player_img.get_width() > WORLD_W // 2 or player_img.get_height() > WORLD_H // 2:
    print("Player image looks very large compared to the map; using fallback small sprite instead.")
    player_img = pygame.Surface((32, 32), pygame.SRCALPHA)
    player_img.fill((200, 50, 50))

# Give the window a title so it's obvious you're running the map/player demo
pygame.display.set_caption("Map - Move the player with Arrow keys / WASD")

# Player setup (world coords) - start centered on the map
player = pygame.Rect(0, 0, player_img.get_width(), player_img.get_height())
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
SHELF_LOCATION = pygame.Rect(344, 68, 25, 56)  # Interaction area from y=68 to y=124

# Shelf interaction variables
SHELF_INVENTORY_SIZE = 20
SHELF_OPEN = False  # Track if shelf interface is open

# Update shelf items with proper names
shelf_items = [
    {"name": "Empty Carts", "quantity": 1, "image": carts_img},
    {"name": "Funnel", "quantity": 1, "image": funnel_img}
]

# Replace player_inventory initialization
player_inventory = [None] * HOTBAR_SIZE  # Initialize with empty slots

def draw_inventory_interface(surf, items, start_x, start_y, max_slots, title=None):
    if title:
        draw_text(surf, title, start_x, start_y - 30, (255, 255, 255))
    
    slot_size = 40
    slots_per_row = 5
    
    for i in range(max_slots):
        x = start_x + (i % slots_per_row) * (slot_size + 10)
        y = start_y + (i // slots_per_row) * (slot_size + 10)
        
        # Draw slot background
        pygame.draw.rect(surf, (100, 100, 100), (x, y, slot_size, slot_size))
        
        # Draw item if exists
        if i < len(items):
            item = items[i]
            # Scale and draw item image
            scaled_img = scale_surface_to_max(item["image"], (slot_size-4, slot_size-4))
            img_x = x + (slot_size - scaled_img.get_width()) // 2
            img_y = y + (slot_size - scaled_img.get_height()) // 2
            surf.blit(scaled_img, (img_x, img_y))
            # Draw quantity
            draw_text(surf, str(item["quantity"]), x + slot_size - 20, y + slot_size - 20, (255, 255, 0))
            # Draw item name below slot
            name_y = y + slot_size + 5
            draw_text(surf, item["name"], x, name_y, (200, 200, 200))

def draw_shelf_interface(surf):
    # Draw semi-transparent full-screen overlay
    overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    surf.blit(overlay, (0, 0))
    
    # Draw only shelf inventory (removed player inventory section)
    draw_inventory_interface(surf, shelf_items, SCREEN_W//4, SCREEN_H//4, SHELF_INVENTORY_SIZE, "Shelf Items")
    
    # Draw instructions - remove global reference since constant is already global
    if not TUTORIAL_DONE:
        draw_text(surf, "Drag items between shelf and hotbar", SCREEN_W//2 - 150, SCREEN_H - 40, (255, 255, 0))

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

class GroundItem:
    def __init__(self, item, x, y):
        self.item = item
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 32, 32)  # Collision rect for pickup

# Add before main()
def get_item_drop_position(player_rect):
    # Drop item slightly in front of player
    return (player_rect.centerx, player_rect.centery + 40)

def draw_ground_items(surf, cam_x, cam_y):
    for ground_item in GROUND_ITEMS:
        # Draw item image
        scaled_img = scale_surface_to_max(ground_item.item["image"], (32, 32))
        screen_x = ground_item.x - cam_x - scaled_img.get_width()//2
        screen_y = ground_item.y - cam_y - scaled_img.get_height()//2
        surf.blit(scaled_img, (screen_x, screen_y))

def find_closest_item(player_rect):
    for ground_item in GROUND_ITEMS:
        # Convert ground item position to be relative to player's world position
        dist_x = abs(player_rect.centerx - ground_item.x)
        dist_y = abs(player_rect.centery - ground_item.y)
        if dist_x < PICKUP_RANGE and dist_y < PICKUP_RANGE:
            return ground_item
    return None

def main():
    running = True
    inside_house = False
    global SHELF_OPEN, DRAGGING_ITEM, TUTORIAL_DONE
    
    # Start player in center of map
    player.x = WORLD_W // 2 - player.width // 2
    player.y = WORLD_H // 2 - player.height // 2

    while running:
        dt = clock.tick(60) / 1000.0  # seconds
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
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
                    if inside_house and not SHELF_OPEN:
                        shelf_in_view = pygame.Rect(
                            SHELF_LOCATION.x - cam_x,
                            SHELF_LOCATION.y - cam_y,
                            SHELF_LOCATION.width,
                            SHELF_LOCATION.height
                        )
                        if shelf_in_view.colliderect(player):
                            SHELF_OPEN = True
                    elif SHELF_OPEN:
                        SHELF_OPEN = False
                    elif not inside_house:
                        # Existing house entrance logic
                        if HOUSE_ENTRANCE.colliderect(player):
                            inside_house = True
                            # Place player at bottom middle of house interior
                            player.x = HOUSE_W // 2 - player.width // 2
                            player.y = HOUSE_H - player.height - 50
                
                elif event.key == pygame.K_ESCAPE:
                    if SHELF_OPEN:
                        SHELF_OPEN = False
                    elif inside_house:
                        # Exit house
                        inside_house = False
                        # Place player just outside house entrance
                        player.x = HOUSE_ENTRANCE.x + HOUSE_ENTRANCE.width
                        player.y = HOUSE_ENTRANCE.y + HOUSE_ENTRANCE.height
                    else:
                        # Only quit game if outside
                        running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    if SHELF_OPEN:
                        # Handle shelf inventory clicks
                        idx = handle_inventory_click(mouse_pos, shelf_items, SHELF_INVENTORY_SIZE, 
                                                  SCREEN_W//4, SCREEN_H//4)
                        if idx is not None and idx < len(shelf_items):
                            DRAGGING_ITEM = shelf_items.pop(idx)
                    
                    # Handle hotbar clicks
                    slot = get_hotbar_slot_at(mouse_pos)
                    if slot is not None:
                        if DRAGGING_ITEM:
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
                        # Drop item on ground
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
        if inside_house:
            screen.blit(house_interior, (-cam_x, -cam_y))
        else:
            screen.blit(bg, (-cam_x, -cam_y))
        
        # Draw ground items before player
        draw_ground_items(screen, cam_x, cam_y)
        screen.blit(player_img, (player.x - cam_x, player.y - cam_y))

        # UI
        draw_text(screen, "Move: Arrow keys / WASD   Enter/Exit: E/ESC   Quit: Close", 10, 10)
        if inside_house:
            # Show shelf interaction prompt when near
            shelf_in_view = pygame.Rect(
                SHELF_LOCATION.x - cam_x,
                SHELF_LOCATION.y - cam_y,
                SHELF_LOCATION.width,
                SHELF_LOCATION.height
            )
            if shelf_in_view.colliderect(player) and not SHELF_OPEN:
                draw_centered_popup(screen, "Press E to open shelf")
            
            # Draw exit instruction
            draw_text(screen, "Press ESC to leave house", SCREEN_W - 200, 10, color=(255, 255, 0))
            
            # Draw shelf inventory if open
            if SHELF_OPEN:
                draw_shelf_interface(screen)
        
        elif HOUSE_ENTRANCE.colliderect(player):
            # Show enter house popup only when outside near entrance
            draw_centered_popup(screen, "Press E to enter house")
        
        # Debug: show player world coordinates and FPS
        draw_text(screen, f"Player: {player.x},{player.y}  FPS: {int(clock.get_fps())}", 10, 30)

        # Draw hotbar
        draw_hotbar(screen)
        
        # Draw dragged item last so it's on top
        if DRAGGING_ITEM:
            draw_dragged_item(screen, DRAGGING_ITEM, mouse_pos)

        # Show pickup prompt if near item
        closest_item = find_closest_item(player)
        if closest_item:
            draw_centered_popup(screen, f"{closest_item.item['name']} - Press E to pick up")

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
