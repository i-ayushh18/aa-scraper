"""
Verification Challenge Handler
Handles CAPTCHA, Incapsula, and AA-specific verification challenges
"""
import undetected_chromedriver as uc
import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger(__name__)


class VerificationHandler:
    """Handles various verification challenges"""
    
    def __init__(self, driver: uc.Chrome, human_behavior):
        self.driver = driver
        self.human_behavior = human_behavior
    
    def handle_verification_challenges(self) -> None:
        """Main method to detect and handle verification challenges"""
        try:
            logger.info("ENHANCED verification challenge detection starting...")
            time.sleep(5)  # Wait for potential challenge to load
            
            current_url = self.driver.current_url
            page_title = self.driver.title
            page_source = self.driver.page_source.lower()
            
            logger.info(f"Current URL: {current_url}")
            logger.info(f"Page title: {page_title}")
            
            # Enhanced detection - check page source first
            verification_keywords = [
                'pardon our interruption',
                'click to verify', 
                'something about your browser made us think you were a bot',
                'verify you are human',
                'human verification',
                'security check',
                'captcha',
                'bot detection',
                'incapsula',
                'imperva', 
                'incident_id',
                'request unsuccessful',
                '_incapsula_resource',
                'main-iframe'
            ]
            
            found_keywords = [keyword for keyword in verification_keywords if keyword in page_source]
            
            if found_keywords:
                logger.warning(f"VERIFICATION DETECTED! Found keywords: {found_keywords}")
                
                # Determine challenge type and handle accordingly
                if any(keyword in found_keywords for keyword in ['incapsula', 'imperva', 'incident_id', '_incapsula_resource']):
                    logger.warning("INCAPSULA/IMPERVA challenge detected!")
                    success = self.bypass_incapsula_challenge()
                else:
                    logger.warning("AA.com verification challenge detected!")
                    success = self.bypass_aa_verification()
                
                if success:
                    logger.info("SUCCESS: Verification challenge bypassed!")
                else:
                    logger.warning("Verification bypass failed")
            else:
                logger.info("No verification challenge detected - proceeding normally")
                
        except Exception as e:
            logger.warning(f"Error in verification detection: {e}")
    
    def bypass_aa_verification(self) -> bool:
        """Enhanced bypass for AA.com 'Click to verify' challenge"""
        try:
            logger.info("ENHANCED AA.com verification bypass starting...")
            
            # Wait for verification page to fully load
            self.human_behavior.human_delay(3, 5)
            
            # Strategy 1: Enhanced "Click to verify" detection
            verification_attempts = [
                {
                    "name": "Exact text matching",
                    "selectors": [
                        "//button[normalize-space(text())='Click to verify']",
                        "//div[normalize-space(text())='Click to verify']",
                        "//span[normalize-space(text())='Click to verify']",
                        "//*[normalize-space(text())='Click to verify']"
                    ]
                },
                {
                    "name": "Partial text matching", 
                    "selectors": [
                        "//button[contains(text(), 'Click to verify')]",
                        "//div[contains(text(), 'Click to verify')]",
                        "//*[contains(text(), 'Click to verify')]"
                    ]
                },
                {
                    "name": "Role-based detection",
                    "selectors": [
                        "//div[@role='button'][contains(text(), 'verify')]",
                        "//*[@role='button'][contains(text(), 'verify')]"
                    ]
                }
            ]
            
            # Try each approach systematically
            for attempt in verification_attempts:
                logger.info(f"Trying {attempt['name']}...")
                
                for selector in attempt['selectors']:
                    try:
                        element = WebDriverWait(self.driver, 3).until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                        
                        if element.is_displayed() and element.is_enabled():
                            logger.info(f"Found verification element: {selector}")
                            
                            # Enhanced human-like interaction
                            self.human_behavior.enhanced_human_click(element)
                            
                            # Wait for verification processing
                            logger.info("Waiting for verification to process...")
                            self.human_behavior.human_delay(5, 8)
                            
                            # Check success
                            if self._check_verification_success():
                                logger.info("SUCCESS: Verification bypassed!")
                                return True
                                
                    except Exception as e:
                        logger.debug(f"Selector {selector} failed: {e}")
                        continue
            
            # Strategy 2: Advanced JavaScript bypass
            logger.info("Trying advanced JavaScript bypass...")
            
            js_result = self.driver.execute_script("""
            console.log('Advanced verification bypass starting...');
            
            // Look for elements with verification text
            var allElements = document.querySelectorAll('*');
            var targetTexts = ['Click to verify', 'CLICK TO VERIFY', 'click to verify', 'Verify', 'Continue'];
            
            for (var i = 0; i < allElements.length; i++) {
                var element = allElements[i];
                var text = (element.textContent || element.innerText || '').trim();
                
                for (var j = 0; j < targetTexts.length; j++) {
                    if (text === targetTexts[j] || text.toLowerCase().includes(targetTexts[j].toLowerCase())) {
                        console.log('Found verification element by text:', element, 'Text:', text);
                        element.click();
                        return 'SUCCESS: Clicked verification element by text: ' + text;
                    }
                }
            }
            
            return 'FAILED: No verification elements found';
            """)
            
            logger.info(f"JavaScript result: {js_result}")
            
            if "SUCCESS" in js_result:
                logger.info("JavaScript bypass successful!")
                self.human_behavior.human_delay(5, 8)
                if self._check_verification_success():
                    return True
            
            logger.warning("All verification bypass attempts failed")
            return False
            
        except Exception as e:
            logger.error(f"AA verification bypass failed: {e}")
            return False
    
    def bypass_incapsula_challenge(self) -> bool:
        """Bypass Incapsula/Imperva security challenge"""
        try:
            logger.info("Attempting Incapsula/Imperva bypass...")
            
            # Strategy 1: Wait for automatic resolution
            logger.info("Waiting for automatic Incapsula resolution...")
            max_wait = 30
            start_time = time.time()
            
            while time.time() - start_time < max_wait:
                try:
                    current_url = self.driver.current_url
                    page_source = self.driver.page_source.lower()
                    
                    # Check if we're past the Incapsula challenge
                    if not any(indicator in page_source for indicator in ['incapsula', 'incident_id', '_incapsula_resource']):
                        # Check if we have flight-related content or are back on AA.com
                        if any(indicator in page_source for indicator in ['flight', 'booking', 'aa.com', 'american airlines']):
                            logger.info("Incapsula challenge resolved automatically!")
                            return True
                    
                    # Still in challenge, wait a bit more
                    logger.info(f"Still in Incapsula challenge... waiting ({int(time.time() - start_time)}s)")
                    self.human_behavior.human_delay(2, 4)
                    
                except Exception as e:
                    logger.debug(f"Error checking Incapsula status: {e}")
                    self.human_behavior.human_delay(2, 4)
            
            logger.warning("Incapsula challenge persisted - trying refresh")
            
            # Strategy 2: Try refreshing the page
            try:
                self.driver.refresh()
                self.human_behavior.human_delay(5, 8)
                
                if self._check_incapsula_resolved():
                    return True
                    
            except Exception as e:
                logger.debug(f"Refresh strategy failed: {e}")
            
            logger.warning("All Incapsula bypass strategies failed")
            return False
            
        except Exception as e:
            logger.error(f"Incapsula bypass failed: {e}")
            return False
    
    def _check_verification_success(self) -> bool:
        """Check if verification challenge was successfully bypassed"""
        try:
            logger.info("Checking verification success...")
            
            # Wait for page transition
            self.human_behavior.human_delay(3, 5)
            
            page_source = self.driver.page_source.lower()
            current_url = self.driver.current_url.lower()
            page_title = self.driver.title.lower()
            
            # Success indicators
            success_indicators = [
                'flight', 'flights', 'search results', 'departure', 'arrival',
                'booking', 'find flights', 'select flight', 'choose flight',
                'aa.com/booking', 'aa.com/flight', 'aa.com/search',
                'from:', 'to:', 'depart:', 'return:', 'passengers:',
                'one way', 'round trip', 'multi-city',
                'nonstop', 'connecting', 'duration', 'price',
                'main cabin', 'first class', 'business class'
            ]
            
            # Failure indicators
            verification_indicators = [
                'pardon our interruption', 'click to verify', 'something about your browser',
                'made us think you were a bot', 'captcha', 'human verification',
                'security check', 'verify you are human', 'please verify',
                'are you human', 'bot detection', 'unusual traffic'
            ]
            
            # Check for success
            verification_gone = not any(indicator in page_source for indicator in verification_indicators)
            has_flight_content = any(indicator in page_source for indicator in success_indicators)
            url_looks_good = any(pattern in current_url for pattern in ['booking', 'flight', 'search', 'results'])
            title_looks_good = any(pattern in page_title for pattern in ['book', 'flight', 'search', 'american airlines'])
            
            if verification_gone and has_flight_content:
                logger.info("Verification SUCCESS: Found flight content, no verification indicators")
                return True
            elif verification_gone and url_looks_good:
                logger.info("Verification SUCCESS: URL indicates success")
                return True
            elif verification_gone and title_looks_good:
                logger.info("Verification SUCCESS: Page title indicates success")
                return True
            elif has_flight_content:
                logger.info("Verification SUCCESS: Found flight content")
                return True
            elif verification_gone:
                logger.info("Verification SUCCESS: Verification page gone")
                return True
            else:
                logger.info(f"Still on verification page. URL: {current_url[:100]}")
                return False
                
        except Exception as e:
            logger.warning(f"Error checking verification success: {e}")
            return False
    
    def _check_incapsula_resolved(self) -> bool:
        """Check if Incapsula challenge is resolved"""
        try:
            page_source = self.driver.page_source.lower()
            current_url = self.driver.current_url.lower()
            
            # Check if Incapsula indicators are gone
            incapsula_gone = not any(indicator in page_source for indicator in [
                'incapsula', 'incident_id', '_incapsula_resource', 'request unsuccessful'
            ])
            
            # Check if we have legitimate content
            has_content = any(indicator in page_source for indicator in [
                'flight', 'booking', 'search', 'american airlines', 'aa.com'
            ])
            
            if incapsula_gone and has_content:
                logger.info("Incapsula challenge resolved - found legitimate content")
                return True
            elif incapsula_gone:
                logger.info("Incapsula indicators gone - likely resolved")
                return True
            else:
                logger.debug("Still blocked by Incapsula")
                return False
                
        except Exception as e:
            logger.debug(f"Error checking Incapsula resolution: {e}")
            return False
    
