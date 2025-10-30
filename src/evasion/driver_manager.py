"""
Chrome Driver Manager with Advanced Stealth Configuration
Handles driver initialization and anti-detection setup
"""
import undetected_chromedriver as uc
import time
import random
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class DriverManager:
    """Manages Chrome driver with advanced stealth configuration"""
    
    def __init__(self):
        self.driver: Optional[uc.Chrome] = None
    
    def create_stealth_driver(self) -> uc.Chrome:
        """Create Chrome driver with ANTI-INCAPSULA stealth configuration"""
        
        for attempt in range(3):
            try:
                logger.info(f"Driver initialization attempt {attempt + 1}/3")
                
                options = self._get_chrome_options()
                driver = uc.Chrome(options=options, version_main=None, driver_executable_path=None)
                time.sleep(3)
                
                # Clear all cookies and storage
                self._clear_browser_data(driver)
                
                # Apply ultimate stealth JavaScript
                self._apply_stealth_javascript(driver)
                
                # Set realistic window size
                driver.set_window_size(1366, 768)
                
                # Test driver
                driver.get("https://httpbin.org/user-agent")
                time.sleep(1)
                
                logger.info(f"Stealth Chrome driver initialized (attempt {attempt + 1})")
                self.driver = driver
                return driver
                
            except Exception as e:
                logger.warning(f"Driver initialization attempt {attempt + 1} failed: {e}")
                if attempt == 2:
                    raise
                continue
        
        raise Exception("All driver initialization attempts failed")
    
    def _get_chrome_options(self) -> uc.ChromeOptions:
        """Configure Chrome options for stealth operation"""
        options = uc.ChromeOptions()
        
        # Check if running in Docker environment
        import os
        is_docker = os.path.exists('/.dockerenv') or os.environ.get('DOCKER_ENV') == 'true'
        
        # Fresh session flags to avoid cookie contamination
        fresh_session_flags = [
            '--disable-blink-features=AutomationControlled',
            '--no-sandbox',
            '--disable-dev-shm-usage',
            '--disable-web-security',
            '--disable-features=VizDisplayCompositor',
            '--disable-extensions',
            '--disable-plugins',
            '--disable-images',
            '--disable-javascript-harmony-shipping',
            '--disable-background-timer-throttling',
            '--disable-renderer-backgrounding',
            '--disable-backgrounding-occluded-windows',
            '--disable-client-side-phishing-detection',
            '--disable-sync',
            '--disable-default-apps',
            '--no-first-run',
            '--no-default-browser-check',
            '--disable-popup-blocking'
        ]
        
        # Additional Docker-specific flags
        if is_docker:
            docker_flags = [
                '--headless=new',
                '--disable-gpu',
                '--disable-software-rasterizer',
                '--disable-background-networking',
                '--disable-default-apps',
                '--disable-extensions',
                '--disable-sync',
                '--disable-translate',
                '--hide-scrollbars',
                '--metrics-recording-only',
                '--mute-audio',
                '--no-first-run',
                '--safebrowsing-disable-auto-update',
                '--ignore-ssl-errors',
                '--ignore-certificate-errors',
                '--ignore-certificate-errors-spki-list',
                '--ignore-ssl-errors-spki-list',
                '--remote-debugging-port=9222',
                '--window-size=1366,768'
            ]
            fresh_session_flags.extend(docker_flags)
            logger.info("Docker environment detected - using headless Chrome configuration")
        
        for flag in fresh_session_flags:
            options.add_argument(flag)
        
        # Realistic user agent rotation
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        ]
        
        selected_ua = random.choice(user_agents)
        options.add_argument(f'--user-agent={selected_ua}')
        logger.info(f"Using user agent: {selected_ua[:50]}...")
        
        # Fresh session preferences
        prefs = {
            "profile.default_content_setting_values": {
                "notifications": 2,
                "media_stream": 2,
                "geolocation": 2,
                "plugins": 1,
                "popups": 2,
                "automatic_downloads": 2,
            },
            "profile.managed_default_content_settings": {
                "images": 1
            },
            "profile.default_content_settings": {
                "popups": 0
            },
            "profile.password_manager_enabled": False,
            "credentials_enable_service": False,
            "profile.password_manager_leak_detection": False,
            "autofill.profile_enabled": False,
            "autofill.credit_card_enabled": False,
            "profile.exit_type": "Normal",
            "profile.exited_cleanly": True,
            "browser.cache.disk.enable": False,
            "browser.cache.memory.enable": False,
            "network.cookie.cookieBehavior": 2,
        }
        options.add_experimental_option("prefs", prefs)
        
        return options
    
    def _clear_browser_data(self, driver: uc.Chrome) -> None:
        """Clear all cookies and browser storage"""
        logger.info("Clearing all cookies and browser storage...")
        driver.delete_all_cookies()
        
        driver.execute_script("""
        // Clear all storage types
        if (window.localStorage) window.localStorage.clear();
        if (window.sessionStorage) window.sessionStorage.clear();
        if (window.indexedDB) {
            window.indexedDB.databases().then(databases => {
                databases.forEach(db => window.indexedDB.deleteDatabase(db.name));
            });
        }
        // Clear cache
        if ('caches' in window) {
            caches.keys().then(names => {
                names.forEach(name => caches.delete(name));
            });
        }
        """)
        
        logger.info("Browser storage cleared - fresh session ready")
    
    def _apply_stealth_javascript(self, driver: uc.Chrome) -> None:
        """Apply ultimate stealth JavaScript to hide automation"""
        ultimate_stealth_js = """
        // Remove all webdriver traces
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        delete navigator.__proto__.webdriver;
        
        // Mock realistic navigator properties
        Object.defineProperty(navigator, 'plugins', {
            get: () => [
                {name: 'Chrome PDF Plugin', filename: 'internal-pdf-viewer', description: 'Portable Document Format'},
                {name: 'Chrome PDF Viewer', filename: 'mhjfbmdgcfjbbpaeojofohoefgiehjai', description: 'Portable Document Format'},
                {name: 'Native Client', filename: 'internal-nacl-plugin', description: 'Native Client Executable'}
            ]
        });
        
        Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
        Object.defineProperty(navigator, 'platform', {get: () => 'Win32'});
        Object.defineProperty(navigator, 'hardwareConcurrency', {get: () => 8});
        
        // Mock chrome runtime
        window.chrome = {
            runtime: {
                onConnect: undefined,
                onMessage: undefined
            }
        };
        
        // Mock permissions API
        const originalQuery = window.navigator.permissions.query;
        window.navigator.permissions.query = (parameters) => (
            parameters.name === 'notifications' ?
            Promise.resolve({ state: Notification.permission }) :
            originalQuery(parameters)
        );
        
        // Remove automation indicators
        ['cdc_adoQpoasnfa76pfcZLmcfl_Array', 'cdc_adoQpoasnfa76pfcZLmcfl_Promise', 'cdc_adoQpoasnfa76pfcZLmcfl_Symbol'].forEach(prop => {
            delete window[prop];
        });
        
        // Mock realistic screen properties
        Object.defineProperty(screen, 'availWidth', {get: () => 1366});
        Object.defineProperty(screen, 'availHeight', {get: () => 728});
        Object.defineProperty(screen, 'width', {get: () => 1366});
        Object.defineProperty(screen, 'height', {get: () => 768});
        
        // Add realistic timing
        const originalDateNow = Date.now;
        Date.now = () => originalDateNow() + Math.floor(Math.random() * 100);
        """
        
        driver.execute_script(ultimate_stealth_js)
    
    def quit_driver(self) -> None:
        """Safely quit the driver"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
            finally:
                self.driver = None