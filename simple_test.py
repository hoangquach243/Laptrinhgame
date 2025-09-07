import pygame
import sys

print("🚀 Starting simple pygame test...")

try:
    # Initialize pygame
    pygame.init()
    print("✅ Pygame initialized")
    
    # Create window
    screen = pygame.display.set_mode((400, 300))
    pygame.display.set_caption("TEST - Do you see this window?")
    print("✅ Window created - Should see a window now!")
    
    # Fill with bright color
    screen.fill((255, 0, 0))
    pygame.display.flip()
    print("✅ Red background drawn")
    
    # Keep window open and wait for events
    print("🖱️  Click the window to close, or wait 10 seconds...")
    
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    running = True
    
    while running:
        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("👋 Window closed by user")
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print("🖱️  Mouse clicked!")
                running = False
        
        # Auto close after 10 seconds
        if pygame.time.get_ticks() - start_time > 10000:
            print("⏰ 10 seconds elapsed, closing...")
            running = False
        
        # Blink colors to make it obvious
        if (pygame.time.get_ticks() // 500) % 2:
            screen.fill((255, 0, 0))  # Red
        else:
            screen.fill((0, 255, 0))  # Green
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    print("✅ Test completed successfully!")
    
except Exception as e:
    print(f"❌ Error occurred: {e}")
    import traceback
    traceback.print_exc()
    
print("🏁 Test finished")