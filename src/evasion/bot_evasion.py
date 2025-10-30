"""
Bot Evasion System - 3-Layer Approach
Implements sophisticated evasion techniques to bypass AA.com bot detection
"""
import undetected_chromedriver as uc
import time
import random
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class BotEvasion:
    """3-layer bot evasion system for AA.com"""
    
    def __init__(self, driver: uc.Chrome):
        self.driver = driver
    
    def attempt_direct_access(self, page_parser, verification_handler) -> bool:
        """Attempt 1: Direct approach with complete booking flow"""
        try:
            logger.info("Attempt 1: HUMAN-PACED direct access")
            logger.info("Human behavior: Starting from homepage like a real user...")
            
            # Start from homepage like a human would
            self.driver.get("https://www.aa.com")
            logger.info("Human behavior: Page loading, reading homepage...")
            time.sleep(random.uniform(5, 8))
            
            # Verify we're on a valid AA site
            current_url = self.driver.current_url
            logger.info(f"Direct access - Current URL: {current_url}")
            
            valid_aa_domains = ["aa.com", "americanairlines.com", "americanairlines.in", "americanairlines.co.uk"]
            is_valid_aa_site = any(domain in current_url.lower() for domain in valid_aa_domains)
            
            if not is_valid_aa_site:
                logger.warning(f"Not on AA site! Redirected to: {current_url}")
                return False
            
            # Complete booking flow
            page_parser.handle_cookies()
            time.sleep(random.uniform(2, 4))
            
            page_parser.navigate_to_booking()
            time.sleep(random.uniform(3, 5))
            
            if page_parser.fill_search_form(award_mode=True):
                time.sleep(5)
                verification_handler.handle_verification_challenges()
                return True
            
            return False
            
        except Exception as e:
            logger.warning(f"Direct access failed: {e}")
            return False
    
    def attempt_referrer_spoofing(self, page_parser, verification_handler) -> bool:
        """Attempt 2: Referrer spoofing approach with complete booking flow"""
        try:
            logger.info("Attempt 2: Referrer spoofing approach")
            
            # Clear cookies first
            self.driver.delete_all_cookies()
            time.sleep(2)
            
            # First visit a travel site to establish referrer
            self.driver.get("https://www.kayak.com")
            time.sleep(random.uniform(3, 5))
            
            # Inject referrer and navigate to AA
            self.driver.execute_script("""
            Object.defineProperty(document, 'referrer', {
                get: function() { return 'https://www.kayak.com/flights'; }
            });
            """)
            
            # Navigate to AA homepage with referrer (like coming from Kayak)
            self.driver.get("https://www.aa.com")
            time.sleep(random.uniform(5, 8))
            
            # Verify we're actually on a valid AA site before proceeding
            current_url = self.driver.current_url
            logger.info(f"Current URL after navigation: {current_url}")
            
            valid_aa_domains = ["aa.com", "americanairlines.com", "americanairlines.in", "americanairlines.co.uk"]
            is_valid_aa_site = any(domain in current_url.lower() for domain in valid_aa_domains)
            
            if not is_valid_aa_site:
                logger.warning(f"Not on AA site! Current URL: {current_url}")
                # Force navigation to AA.com
                self.driver.get("https://www.aa.com")
                time.sleep(random.uniform(3, 5))
                current_url = self.driver.current_url
                logger.info(f"After forced navigation: {current_url}")
            
            # Complete booking flow
            page_parser.handle_cookies()
            time.sleep(random.uniform(2, 4))
            
            page_parser.navigate_to_booking()
            time.sleep(random.uniform(3, 5))
            
            if page_parser.fill_search_form(award_mode=True):
                time.sleep(5)
                verification_handler.handle_verification_challenges()
                return True
            
            return False
            
        except Exception as e:
            logger.warning(f"Referrer spoofing failed: {e}")
            return False
    
    def attempt_mobile_access(self, page_parser, verification_handler) -> bool:
        """Attempt 3: Mobile user agent approach with complete booking flow"""
        try:
            logger.info("Attempt 3: Mobile user agent approach")
            
            # Clear cookies first
            self.driver.delete_all_cookies()
            time.sleep(2)
            
            # Switch to mobile user agent
            mobile_ua = "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
            self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                "userAgent": mobile_ua,
                "acceptLanguage": "en-US,en;q=0.9",
                "platform": "iPhone"
            })
            
            # Set mobile viewport
            self.driver.set_window_size(375, 667)  # iPhone size
            
            # Navigate to AA homepage in mobile mode
            self.driver.get("https://www.aa.com")
            time.sleep(random.uniform(5, 8))
            
            # Verify we're on a valid AA site in mobile mode
            current_url = self.driver.current_url
            logger.info(f"Mobile access - Current URL: {current_url}")
            
            valid_aa_domains = ["aa.com", "americanairlines.com", "americanairlines.in", "americanairlines.co.uk"]
            is_valid_aa_site = any(domain in current_url.lower() for domain in valid_aa_domains)
            
            if not is_valid_aa_site:
                logger.warning(f"Not on AA site! Mobile redirected to: {current_url}")
                # Try direct navigation again
                self.driver.get("https://www.aa.com")
                time.sleep(random.uniform(3, 5))
            
            # Keep mobile size for form filling (don't restore desktop yet)
            logger.info("Keeping mobile viewport for form filling...")
            
            # Complete booking flow
            page_parser.handle_cookies()
            time.sleep(random.uniform(2, 4))
            
            page_parser.navigate_to_booking()
            time.sleep(random.uniform(3, 5))
            
            if page_parser.fill_search_form(award_mode=True):
                time.sleep(5)
                verification_handler.handle_verification_challenges()
                return True
            
            return False
            
        except Exception as e:
            logger.warning(f"Mobile access failed: {e}")
            return False
    
    def apply_proactive_evasion(self, step: str) -> None:
        """Apply proactive evasion techniques during scraping"""
        try:
            if "critical" in step.lower():
                logger.info(f"Applying COMPLETE evasion sequence before {step}...")
                
                # Step 1: Clear webdriver properties
                try:
                    self.driver.execute_script("""
                    delete window.navigator.webdriver;
                    delete window.navigator.__webdriver_script_fn;
                    delete window.navigator.__webdriver_evaluate;
                    delete window.navigator.__webdriver_unwrapped;
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => false,
                    });
                    """)
                    time.sleep(random.uniform(1, 2))
                except Exception as e:
                    logger.debug(f"Webdriver clearing failed: {e}")
                
                # Step 2: Referrer spoofing in new tab
                try:
                    original_window = self.driver.current_window_handle
                    original_url = self.driver.current_url
                    logger.info(f"Original window: {original_url}")
                    
                    self.driver.execute_script("window.open('https://www.kayak.com', '_blank');")
                    self.driver.switch_to.window(self.driver.window_handles[-1])
                    time.sleep(random.uniform(2, 4))
                    
                    # Close Kayak tab and switch back
                    self.driver.close()
                    self.driver.switch_to.window(original_window)
                    
                    # CRITICAL: Verify we're back on the AA site
                    current_url = self.driver.current_url
                    valid_aa_domains = ["aa.com", "americanairlines.com", "americanairlines.in", "americanairlines.co.uk"]
                    is_valid_aa_site = any(domain in current_url.lower() for domain in valid_aa_domains)
                    
                    if not is_valid_aa_site:
                        logger.warning(f"Tab switch failed! Still on: {current_url}")
                        # Force navigation back to AA
                        self.driver.get(original_url)
                        time.sleep(2)
                    else:
                        logger.info(f"✅ Successfully switched back to AA site: {current_url}")
                    
                    self.driver.execute_script("""
                    Object.defineProperty(document, 'referrer', {
                        get: function() { return 'https://www.kayak.com/flights'; },
                        configurable: true
                    });
                    """)
                    time.sleep(random.uniform(1, 2))
                except Exception as e:
                    logger.debug(f"Referrer spoofing failed: {e}")
                
                # Step 3: Mobile user agent switching
                try:
                    mobile_ua = "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
                    self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                        "userAgent": mobile_ua,
                        "acceptLanguage": "en-US,en;q=0.9",
                        "platform": "iPhone"
                    })
                    
                    current_size = self.driver.get_window_size()
                    self.driver.set_window_size(375, 667)
                    time.sleep(random.uniform(1, 3))
                    
                    self.driver.set_window_size(current_size['width'], current_size['height'])
                    
                    desktop_ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
                    self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                        "userAgent": desktop_ua
                    })
                except Exception as e:
                    logger.debug(f"Mobile evasion failed: {e}")
                
                # Final cleanup
                try:
                    self.driver.execute_script("""
                    // Clear all webdriver properties
                    delete window.navigator.webdriver;
                    delete window.navigator.__webdriver_script_fn;
                    delete window.navigator.__webdriver_evaluate;
                    delete window.navigator.__webdriver_unwrapped;
                    delete window.navigator.__fxdriver_evaluate;
                    delete window.navigator.__fxdriver_unwrapped;
                    delete window.navigator.__driver_evaluate;
                    delete window.navigator.__selenium_evaluate;
                    delete window.navigator.__webdriver_script_function;
                    
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => false,
                    });
                    """)
                except Exception as e:
                    logger.debug(f"Final cleanup failed: {e}")
                
                time.sleep(random.uniform(2, 5))
                logger.info("COMPLETE evasion sequence applied successfully")
                
            else:
                # Light evasion for non-critical steps
                if random.random() < 0.3:  # 30% chance
                    logger.info(f"Applying light evasion during {step}...")
                    try:
                        self.driver.execute_script("delete window.navigator.webdriver;")
                        time.sleep(random.uniform(0.5, 1.0))
                    except:
                        pass
                        
        except Exception as e:
            logger.debug(f"Proactive evasion failed (non-critical): {e}")
    
    def check_access_denied(self) -> bool:
        """Check if we got access denied or bot detection"""
        try:
            page_source = self.driver.page_source.lower()
            title = self.driver.title.lower()
            
            access_denied_indicators = [
                'access denied',
                'access to this page has been denied',
                'blocked',
                'bot detection',
                'security check',
                'unusual traffic',
                'automated requests',
                'captcha',
                'verify you are human',
                'cloudflare'
            ]
            
            for indicator in access_denied_indicators:
                if indicator in page_source or indicator in title:
                    return True
            
            return False
        except:
            return False