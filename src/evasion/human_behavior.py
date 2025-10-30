"""
Human Behavior Simulation
Implements realistic human-like interactions to avoid bot detection
"""
import undetected_chromedriver as uc
import time
import random
import logging
from selenium.webdriver.common.action_chains import ActionChains

logger = logging.getLogger(__name__)


class HumanBehavior:
    """Simulates realistic human behavior patterns"""
    
    def __init__(self, driver: uc.Chrome):
        self.driver = driver
    
    def human_delay(self, min_seconds: float, max_seconds: float) -> None:
        """Add human-like random delays"""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
    
    def human_click(self, element) -> None:
        """Click element with human-like behavior"""
        try:
            # Scroll to element first (humans look for elements)
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
            self.human_delay(1.0, 2.0)  # Time to "see" the element
            
            # Move mouse to element area (simulate mouse movement)
            self._human_mouse_movement(element)
            self.human_delay(0.3, 0.8)  # Pause before clicking
            
            # Click the element
            element.click()
            
            # Pause after clicking (human waits to see result)
            self.human_delay(0.8, 1.5)
            
        except Exception as e:
            logger.debug(f"Human click failed: {e}")
    
    def enhanced_human_click(self, element) -> None:
        """Enhanced human-like clicking for verification elements"""
        try:
            logger.info("Performing enhanced human-like click...")
            
            # Scroll element into view smoothly
            self.driver.execute_script("""
            arguments[0].scrollIntoView({
                behavior: 'smooth', 
                block: 'center',
                inline: 'center'
            });
            """, element)
            
            # Human reads and processes what they see
            self.human_delay(2.0, 3.5)
            
            # Multiple click attempts (sometimes humans miss)
            click_attempts = [
                lambda: element.click(),
                lambda: self.driver.execute_script("arguments[0].click();", element),
                lambda: self.driver.execute_script("""
                var event = new MouseEvent('click', {
                    view: window,
                    bubbles: true,
                    cancelable: true
                });
                arguments[0].dispatchEvent(event);
                """, element)
            ]
            
            for i, click_method in enumerate(click_attempts):
                try:
                    logger.info(f"Click attempt {i+1}/3...")
                    click_method()
                    logger.info(f"Click method {i+1} executed successfully")
                    break
                except Exception as e:
                    logger.debug(f"Click method {i+1} failed: {e}")
                    if i < len(click_attempts) - 1:
                        self.human_delay(0.5, 1.0)
            
            # Post-click human behavior
            self.human_delay(1.5, 3.0)  # Human waits to see result
            
        except Exception as e:
            logger.warning(f"Enhanced human click failed: {e}")
            # Fallback to regular click
            try:
                element.click()
            except:
                pass
    
    def simulate_human_reading(self) -> None:
        """Simulate human reading/scanning the page"""
        try:
            # Scroll up and down like reading
            self.driver.execute_script("window.scrollTo(0, 100);")
            self.human_delay(1.0, 2.0)
            
            self.driver.execute_script("window.scrollTo(0, 0);")
            self.human_delay(1.5, 2.5)
            
            # Simulate looking around the page
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/3);")
            self.human_delay(1.0, 2.0)
            
        except Exception as e:
            logger.debug(f"Human reading simulation failed: {e}")
    
    def _human_mouse_movement(self, element) -> None:
        """Simulate human-like mouse movement to element"""
        try:
            # Get element location
            location = element.location
            size = element.size
            
            # Calculate center of element
            center_x = location['x'] + size['width'] // 2
            center_y = location['y'] + size['height'] // 2
            
            # Create action chain with human-like movement
            actions = ActionChains(self.driver)
            
            # Move to a random point near the element first
            offset_x = random.randint(-50, 50)
            offset_y = random.randint(-50, 50)
            actions.move_by_offset(offset_x, offset_y)
            
            # Then move to the element
            actions.move_to_element(element)
            
            # Small random delay before click
            actions.pause(random.uniform(0.1, 0.3))
            
            # Perform the movement
            actions.perform()
            
        except Exception as e:
            logger.debug(f"Human mouse movement failed: {e}")
    
    def enhanced_mouse_movement(self, element) -> None:
        """Enhanced mouse movement simulation"""
        try:
            # Get element position and size
            location = element.location
            size = element.size
            
            # Calculate target coordinates (center of element with slight randomness)
            target_x = location['x'] + size['width'] // 2 + random.randint(-10, 10)
            target_y = location['y'] + size['height'] // 2 + random.randint(-5, 5)
            
            # Create realistic mouse path
            actions = ActionChains(self.driver)
            
            # Start from a random position
            start_x = random.randint(100, 500)
            start_y = random.randint(100, 300)
            
            # Move in steps to simulate human mouse movement
            steps = 5
            for i in range(steps):
                intermediate_x = start_x + (target_x - start_x) * (i + 1) / steps
                intermediate_y = start_y + (target_y - start_y) * (i + 1) / steps
                
                # Add slight randomness to path
                intermediate_x += random.randint(-20, 20)
                intermediate_y += random.randint(-10, 10)
                
                actions.move_by_offset(
                    intermediate_x - (start_x if i == 0 else prev_x),
                    intermediate_y - (start_y if i == 0 else prev_y)
                )
                
                prev_x, prev_y = intermediate_x, intermediate_y
                
                # Small delay between movements
                time.sleep(random.uniform(0.1, 0.3))
            
            # Final move to element
            actions.move_to_element(element)
            actions.perform()
            
        except Exception as e:
            logger.debug(f"Enhanced mouse movement failed: {e}")
    
    def human_typing(self, element, text: str) -> None:
        """Type text with human-like patterns"""
        try:
            element.clear()
            time.sleep(0.5)
            
            # Type with realistic delays between characters
            for char in text:
                element.send_keys(char)
                # Random delay between keystrokes (humans type at different speeds)
                time.sleep(random.uniform(0.05, 0.15))
            
            # Pause after typing (human reviews what they typed)
            self.human_delay(0.5, 1.0)
            
        except Exception as e:
            logger.debug(f"Human typing failed: {e}")
            # Fallback to regular typing
            element.clear()
            time.sleep(0.5)
            element.send_keys(text)