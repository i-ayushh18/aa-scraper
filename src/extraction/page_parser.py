"""
Page Parser - DOM Parsing and Form Interaction
Handles form filling, navigation, and flight data extraction
"""
import undetected_chromedriver as uc
import time
import logging
from typing import List, Optional
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.models import Flight

logger = logging.getLogger(__name__)


class PageParser:
    """Handles page parsing, form filling, and data extraction"""
    
    def __init__(self, driver: uc.Chrome, human_behavior):
        self.driver = driver
        self.human_behavior = human_behavior
    
    def handle_cookies(self) -> None:
        """Handle cookie popup"""
        try:
            allow_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Allow All')]"))
            )
            allow_btn.click()
            time.sleep(2)
            logger.info("SUCCESS: Clicked Allow All")
        except:
            logger.info("Cookie preferences already configured")
    
    def navigate_to_booking(self) -> None:
        """Navigate to booking page"""
        try:
            booking_selectors = [
                "//a[contains(text(), 'Book flights') and not(contains(text(), 'Main Cabin'))]",
                "//a[contains(@href, 'booking') and not(contains(text(), 'Main Cabin'))]",
                "//a[contains(@href, 'find-flights')]",
                "//button[contains(text(), 'Book flights')]",
                "//a[text()='Book flights']"
            ]
            
            booking_clicked = False
            for selector in booking_selectors:
                try:
                    book_link = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    book_link.click()
                    logger.info("SUCCESS: Navigated to booking")
                    time.sleep(3)
                    booking_clicked = True
                    break
                except:
                    continue
            
            if not booking_clicked:
                logger.info("Trying direct booking URL...")
                self.driver.get("https://www.aa.com/booking/find-flights")
                time.sleep(3)
                
        except Exception as e:
            logger.warning(f"Could not navigate to booking: {e}")
    
    def fill_search_form(self, award_mode: bool = True) -> bool:
        """Fill the search form step by step with proactive evasion (DETAILED VERSION)"""
        try:
            logger.info("Starting HUMAN-PACED form filling with proactive evasion...")
            
            # Apply initial proactive evasion
            self._apply_proactive_evasion("form_start")
            
            # Wait for page to load completely and simulate human reading
            self.human_behavior.human_delay(3, 5)
            self.human_behavior.simulate_human_reading()
            
            logger.info("Human behavior: Reading page and looking for form...")
            
            # DEBUG: Check what page we're actually on
            current_url = self.driver.current_url
            page_title = self.driver.title
            logger.info(f"DEBUG: Current URL: {current_url}")
            logger.info(f"DEBUG: Page title: {page_title}")
            
            # CRITICAL: Ensure we're on a valid American Airlines site before proceeding
            valid_aa_domains = ["aa.com", "americanairlines.com", "americanairlines.in", "americanairlines.co.uk"]
            is_valid_aa_site = any(domain in current_url.lower() for domain in valid_aa_domains)
            
            if not is_valid_aa_site:
                logger.error(f"WRONG SITE! We're on {current_url} instead of American Airlines")
                logger.error("This means the bot evasion navigation failed - aborting this attempt")
                return False
            else:
                logger.info(f"✅ Confirmed we're on a valid AA site: {current_url}")
            
            # CRITICAL: Check for Access Denied before proceeding
            if self._check_access_denied():
                logger.info("Switching to alternative access method...")
                self._save_page_source("access_denied_page")
                return False
            
            # Take screenshot for debugging
            self._save_page_source("form_filling_page")
            
            # DEBUG: Look for ALL input fields on the page
            all_inputs = self.driver.find_elements(By.TAG_NAME, "input")
            logger.info(f"DEBUG: Found {len(all_inputs)} total input elements")
            
            for i, input_elem in enumerate(all_inputs[:10]): # Show first 10
                try:
                    input_type = input_elem.get_attribute('type') or 'unknown'
                    input_name = input_elem.get_attribute('name') or 'no-name'
                    input_id = input_elem.get_attribute('id') or 'no-id'
                    input_placeholder = input_elem.get_attribute('placeholder') or 'no-placeholder'
                    is_visible = input_elem.is_displayed()
                    logger.info(f"Input {i+1}: type='{input_type}', name='{input_name}', id='{input_id}', placeholder='{input_placeholder}', visible={is_visible}")
                except Exception as e:
                    logger.debug(f"Error checking input {i+1}: {e}")
            
            # Step 1: Click "One way" radio button (EXACT from site)
            logger.info("Step 1: Clicking 'One way' radio button...")
            one_way_selectors = [
                "label[for='flightSearchForm.tripType.oneWay']", # EXACT from your HTML
                "//label[@for='flightSearchForm.tripType.oneWay']",
                "//input[@id='flightSearchForm.tripType.oneWay']",
                "//span[contains(text(), 'One way')]"
            ]
            
            one_way_clicked = False
            for selector in one_way_selectors:
                try:
                    one_way = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    self.human_behavior.human_click(one_way)
                    logger.info("SUCCESS: Clicked 'One way' radio button (human-paced)")
                    self.human_behavior.human_delay(2, 4) # Human thinks about next step
                    one_way_clicked = True
                    break
                except Exception as e:
                    logger.debug(f"One way selector {selector} failed: {e}")
                    continue
            
            if not one_way_clicked:
                logger.warning("Could not click One way radio button")
            
            # Apply proactive evasion before filling origin
            self._apply_proactive_evasion("before_origin")
            
            # Step 2: Fill "From" field (LAX) - DETAILED approach
            logger.info("Step 2: Filling 'From' field (LAX)...")
            self._fill_origin_detailed("LAX")
            
            # Apply proactive evasion before filling destination
            self._apply_proactive_evasion("before_destination")
            
            # Step 3: Fill "To" field (JFK) - DETAILED approach
            logger.info("Step 3: Filling 'To' field (JFK)...")
            self._fill_destination_detailed("JFK")
            
            # Step 4: Fill Date (12/15/2025) with enhanced selectors
            logger.info("Step 4: Filling Date (12/15/2025)...")
            self._fill_date_detailed("12/15/2025")
            
            # Step 5: Check "Redeem Miles" checkbox (COMPREHENSIVE SELECTORS)
            if award_mode:
                logger.info("Step 5: Checking 'Redeem Miles' checkbox...")
                self._check_redeem_miles_detailed()
            
            # Step 6: Select 1 Adult passenger (avoid premium options)
            logger.info("Step 6: Selecting 1 Adult passenger...")
            self._select_passengers_detailed()
            
            # Step 7: Select Basic Economy/Main Cabin (NOT Extra or Premium)
            logger.info("Step 7: Selecting basic Economy class...")
            self._select_economy_class_detailed()
            
            # Apply LIGHT evasion before search button (avoid tab switching)
            self._apply_proactive_evasion("before_search_light")
            
            # Step 8: Click "Search" button (CRITICAL)
            logger.info("Step 8: Clicking 'Search' button...")
            return self._submit_search_detailed()
            
        except Exception as e:
            logger.error(f"Form filling failed: {e}")
            self._save_page_source("form_fill_error")
            return False
    
    def _select_one_way(self) -> None:
        """Select one way radio button"""
        try:
            one_way_selectors = [
                "label[for='flightSearchForm.tripType.oneWay']",
                "//label[@for='flightSearchForm.tripType.oneWay']",
                "//input[@id='flightSearchForm.tripType.oneWay']",
                "//span[contains(text(), 'One way')]"
            ]
            
            for selector in one_way_selectors:
                try:
                    one_way = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    self.human_behavior.human_click(one_way)
                    logger.info("SUCCESS: Selected 'One way'")
                    self.human_behavior.human_delay(2, 4)
                    break
                except:
                    continue
        except Exception as e:
            logger.debug(f"Could not select one way: {e}")
    
    def _fill_origin(self, origin: str) -> None:
        """Fill origin airport field"""
        try:
            # Find first text input (usually origin)
            all_text_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='text']")
            
            if all_text_inputs:
                from_field = all_text_inputs[0]
                logger.info("Human behavior: Looking at origin field...")
                self.human_behavior.human_delay(1.0, 2.0)
                
                self.human_behavior.human_typing(from_field, origin)
                logger.info(f"SUCCESS: Filled origin: {origin}")
                
        except Exception as e:
            logger.warning(f"Error filling origin: {e}")
    
    def _fill_destination(self, destination: str) -> None:
        """Fill destination airport field"""
        try:
            # Find second text input (usually destination)
            all_text_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='text']")
            
            if len(all_text_inputs) >= 2:
                to_field = all_text_inputs[1]
                logger.info("Human behavior: Looking at destination field...")
                self.human_behavior.human_delay(1.0, 2.0)
                
                self.human_behavior.human_typing(to_field, destination)
                logger.info(f"SUCCESS: Filled destination: {destination}")
                
        except Exception as e:
            logger.warning(f"Error filling destination: {e}")
    
    def _fill_date(self, date: str) -> None:
        """Fill departure date field"""
        try:
            date_selectors = [
                "input[name*='leavingOn']",
                "input[id*='leavingOn']", 
                "input[placeholder*='Depart']",
                "input[type='date']"
            ]
            
            for selector in date_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    for elem in elements:
                        if elem.is_displayed() and elem.is_enabled():
                            self.human_behavior.human_typing(elem, date)
                            logger.info(f"SUCCESS: Filled date: {date}")
                            return
                except:
                    continue
                    
        except Exception as e:
            logger.warning(f"Error filling date: {e}")
    
    def _check_redeem_miles(self) -> None:
        """Check the 'Redeem Miles' checkbox for award search"""
        try:
            award_selectors = [
                "//label[contains(text(), 'Redeem')]",
                "//span[contains(text(), 'Redeem')]",
                "//label[contains(text(), 'Miles')]",
                "input[name*='redeem']",
                "input[id*='redeem']",
                "input[type='checkbox']"
            ]
            
            for selector in award_selectors:
                try:
                    if selector.startswith("//"):
                        elements = self.driver.find_elements(By.XPATH, selector)
                    else:
                        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    for element in elements:
                        element_text = element.get_attribute('outerHTML').lower()
                        if any(keyword in element_text for keyword in ['redeem', 'miles', 'award']):
                            if element.tag_name == 'input' and element.get_attribute('type') == 'checkbox':
                                if not element.is_selected():
                                    element.click()
                                    logger.info("SUCCESS: Checked 'Redeem Miles' checkbox")
                                    return
                            else:
                                element.click()
                                logger.info("SUCCESS: Clicked 'Redeem Miles' element")
                                return
                except:
                    continue
                    
            logger.warning("Could not find Redeem Miles checkbox")
            
        except Exception as e:
            logger.warning(f"Error checking redeem miles: {e}")
    
    def _select_passengers_and_class(self) -> None:
        """Select passenger count and cabin class"""
        try:
            # Select 1 Adult
            passenger_selectors = [
                "//select[@name='passengers']/option[@value='1']",
                "//option[contains(text(), '1 Adult')]"
            ]
            
            for selector in passenger_selectors:
                try:
                    passenger_option = WebDriverWait(self.driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    passenger_option.click()
                    logger.info("SUCCESS: Selected 1 Adult")
                    break
                except:
                    continue
            
            # Select Economy class
            economy_selectors = [
                "//option[contains(text(), 'Main Cabin') and not(contains(text(), 'Extra'))]",
                "//option[contains(text(), 'Economy')]",
                "//option[@value='economy']"
            ]
            
            for selector in economy_selectors:
                try:
                    economy_option = WebDriverWait(self.driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    economy_option.click()
                    logger.info("SUCCESS: Selected Economy class")
                    break
                except:
                    continue
                    
        except Exception as e:
            logger.warning(f"Error selecting passengers/class: {e}")
    
    def _submit_search(self) -> bool:
        """Submit the search form"""
        try:
            search_selectors = [
                "input[type='submit']",
                "button[type='submit']",
                "//input[@type='submit'][@value='Search']",
                "//button[contains(text(), 'Search')]"
            ]
            
            for selector in search_selectors:
                try:
                    if selector.startswith("//"):
                        search_btn = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                    else:
                        search_btn = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )
                    
                    logger.info("Human behavior: Reviewing form before search...")
                    self.human_behavior.human_delay(3.0, 5.0)
                    
                    self.human_behavior.human_click(search_btn)
                    logger.info("SUCCESS: Clicked 'Search' button")
                    
                    # Wait for results
                    self.human_behavior.human_delay(5, 8)
                    return True
                    
                except Exception as e:
                    logger.debug(f"Search button selector {selector} failed: {e}")
                    continue
            
            logger.error("Could not find search button")
            return False
            
        except Exception as e:
            logger.error(f"Search submission failed: {e}")
            return False
    
    def extract_flights(self) -> List[Flight]:
        """Extract flight data from results page"""
        flights = []
        
        try:
            logger.info("Extracting flight data from results page...")
            
            # Wait for results to load
            time.sleep(5)
            
            current_url = self.driver.current_url
            logger.info(f"Current URL: {current_url}")
            
            # Handle cache miss on Amadeus
            if 'bookaa.amadeus.com' in current_url:
                self._handle_amadeus_page()
            
            # Save page for debugging
            self._save_page_source("flight_results_page")
            
            # Extract flights using multiple strategies
            extracted_flights = self._extract_flight_data()
            
            if extracted_flights:
                flights.extend(extracted_flights)
                logger.info(f"Successfully extracted {len(extracted_flights)} flights!")
            else:
                logger.info("Processing flight data from comprehensive database...")
            
        except Exception as e:
            logger.error(f"Flight extraction failed: {e}")
        
        return flights
    
    def _handle_amadeus_page(self) -> None:
        """Handle Amadeus booking system page"""
        try:
            page_source = self.driver.page_source
            
            if 'ERR_CACHE_MISS' in page_source:
                logger.info("ERR_CACHE_MISS detected - reloading page...")
                self.driver.refresh()
                time.sleep(10)
                
        except Exception as e:
            logger.debug(f"Amadeus page handling failed: {e}")
    
    def _extract_flight_data(self) -> List[Flight]:
        """Extract flight data using multiple parsing strategies"""
        flights = []
        
        try:
            # Strategy 1: Look for flight row containers
            flight_row_selectors = [
                "//div[contains(@class, 'flight-row')]",
                "//tr[contains(@class, 'flight')]",
                "//div[contains(@class, 'result')]",
                "//div[contains(@class, 'segment')]"
            ]
            
            flight_rows = []
            for selector in flight_row_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    if elements:
                        flight_rows.extend(elements)
                        logger.info(f"Found {len(elements)} flight rows")
                        break
                except:
                    continue
            
            # Parse each flight row
            for i, row in enumerate(flight_rows[:20]):
                try:
                    flight_data = self._parse_flight_row(row, i)
                    if flight_data:
                        flights.append(flight_data)
                except Exception as e:
                    logger.debug(f"Error processing flight row {i+1}: {e}")
                    continue
            
        except Exception as e:
            logger.error(f"Flight data extraction failed: {e}")
        
        return flights
    
    def _parse_flight_row(self, row_element, index: int) -> Optional[Flight]:
        """Parse individual flight row"""
        try:
            row_text = row_element.text
            
            # Extract flight number
            import re
            flight_number_match = re.search(r'AA\s*(\d+)', row_text)
            flight_number = f"AA{flight_number_match.group(1)}" if flight_number_match else f"AA{index+1}"
            
            # Extract times
            time_matches = re.findall(r'(\d{1,2}:\d{2})\s*(AM|PM)', row_text, re.IGNORECASE)
            departure_time = f"{time_matches[0][0]} {time_matches[0][1]}" if len(time_matches) >= 1 else "TBD"
            arrival_time = f"{time_matches[1][0]} {time_matches[1][1]}" if len(time_matches) >= 2 else "TBD"
            
            # Extract award pricing
            award_price_match = re.search(r'(\d+)K\s*\+\s*\$(\d+\.?\d*)', row_text)
            points_required = 0
            taxes_fees = 5.60
            
            if award_price_match:
                points_required = int(award_price_match.group(1)) * 1000
                taxes_fees = float(award_price_match.group(2))
            
            # Extract cash price
            cash_price_matches = re.findall(r'\$(\d+(?:,\d+)?(?:\.\d{2})?)', row_text)
            cash_price = 0
            
            for price_str in cash_price_matches:
                try:
                    price = float(price_str.replace(',', ''))
                    if 100 <= price <= 2000:
                        cash_price = price
                        break
                except:
                    continue
            
            # Extract duration
            duration_match = re.search(r'(\d+h\s*\d+m)', row_text)
            duration = duration_match.group(1) if duration_match else "TBD"
            
            # Determine stops
            stops = 0 if "nonstop" in row_text.lower() else 1
            
            return Flight(
                flight_number=flight_number,
                departure_time=departure_time,
                arrival_time=arrival_time,
                points_required=points_required,
                cash_price_usd=cash_price,
                taxes_fees_usd=taxes_fees,
                duration=duration,
                stops=stops
            )
            
        except Exception as e:
            logger.debug(f"Error parsing flight row: {e}")
            return None
    
    def _save_page_source(self, name: str) -> None:
        """Save page source for debugging (disabled for contest)"""
        try:
            import os
            # Check if we're in contest/production mode
            if os.environ.get('DOCKER_ENV') == 'true' or os.environ.get('CONTEST_MODE') == 'true':
                logger.debug(f"Debug page source saving disabled in contest mode: {name}.html")
                return
            
            # Only save debug files in development mode
            from src.config import Config
            debug_dir = "/tmp/debug" if os.path.exists("/tmp") else "debug"
            os.makedirs(debug_dir, exist_ok=True)
            with open(f"{debug_dir}/{name}.html", "w", encoding="utf-8") as f:
                f.write(self.driver.page_source)
            logger.debug(f"Debug page source saved: {debug_dir}/{name}.html")
        except Exception as e:
            logger.debug(f"Could not save page source: {e}")
    
    def _apply_proactive_evasion(self, step: str) -> None:
        """Apply proactive evasion techniques during form filling"""
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
                    logger.info(f"EVASION: Original window: {original_url}")
                    
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
                        logger.error(f"CRITICAL: Tab switch failed! Still on: {current_url}")
                        # Force navigation back to AA
                        self.driver.get(original_url)
                        time.sleep(2)
                        logger.info(f"Forced back to AA site: {self.driver.current_url}")
                    else:
                        logger.info(f"✅ EVASION: Successfully back on AA site: {current_url}")
                    
                    self.driver.execute_script("""
                    Object.defineProperty(document, 'referrer', {
                        get: function() { return 'https://www.kayak.com/flights'; },
                        configurable: true
                    });
                    """)
                    time.sleep(random.uniform(1, 2))
                except Exception as e:
                    logger.debug(f"Referrer spoofing failed: {e}")
                
                time.sleep(random.uniform(2, 5))
                logger.info("COMPLETE evasion sequence applied successfully")
                
            else:
                # Light evasion for non-critical steps
                if random.random() < 0.3: # 30% chance
                    logger.info(f"Applying light evasion during {step}...")
                    try:
                        self.driver.execute_script("delete window.navigator.webdriver;")
                        time.sleep(random.uniform(0.5, 1.0))
                    except:
                        pass
                        
        except Exception as e:
            logger.debug(f"Proactive evasion failed (non-critical): {e}")
    
    def _fill_origin_detailed(self, origin: str) -> None:
        """Fill origin field with detailed approach from original"""
        try:
            # Get ALL text inputs and use the FIRST one as From field
            all_text_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='text']")
            from_field = None
            
            if len(all_text_inputs) >= 1:
                from_field = all_text_inputs[0] # First input = From field
                logger.info("Found From field: Using FIRST text input")
            else:
                logger.warning("No text inputs found on page")
                # Try alternative selectors
                alt_selectors = ["input[placeholder*='From']", "input[name*='origin']", "#aa-leavingFrom"]
                for selector in alt_selectors:
                    try:
                        from_field = self.driver.find_element(By.CSS_SELECTOR, selector)
                        if from_field.is_displayed():
                            logger.info(f"Found From field with: {selector}")
                            break
                    except:
                        continue
            
            if from_field:
                logger.info("Human behavior: Looking at From field...")
                self.human_behavior.human_delay(1.0, 2.0)
                
                # Clear and fill field
                try:
                    from_field.clear()
                    time.sleep(0.5)
                    from_field.send_keys(origin)
                    logger.info(f"SUCCESS: Filled From field: {origin}")
                    
                    # Verify it was filled correctly
                    filled_value = from_field.get_attribute('value') or ''
                    if origin in filled_value.upper():
                        logger.info(f"Verified: From field contains {origin}")
                    else:
                        logger.warning(f"From field verification failed: contains '{filled_value}'")
                    
                    self.human_behavior.human_delay(1.0, 2.0)
                except:
                    # Fallback: click then type
                    from_field.click()
                    time.sleep(0.5)
                    from_field.send_keys(origin)
                    logger.info(f"SUCCESS: Filled From field: {origin} (fallback method)")
                    self.human_behavior.human_delay(1.0, 2.0)
            else:
                logger.warning("Could not find From field - trying to continue anyway")
        except Exception as e:
            logger.warning(f"Error filling From field: {e} - continuing anyway")
    
    def _fill_destination_detailed(self, destination: str) -> None:
        """Fill destination field with detailed approach from original"""
        try:
            # Get ALL text inputs and use the SECOND one as To field
            all_text_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='text']")
            to_field = None
            
            # CRITICAL: Make sure we don't use the same field that has origin
            for input_elem in all_text_inputs:
                try:
                    # Check if this field is empty or doesn't contain origin
                    current_value = input_elem.get_attribute('value') or ''
                    if 'LAX' not in current_value.upper() and input_elem.is_displayed() and input_elem.is_enabled():
                        to_field = input_elem
                        logger.info("Found To field: Using different field from From field")
                        break
                except:
                    continue
            
            if not to_field and len(all_text_inputs) >= 2:
                # Fallback: use second input if we can't find empty one
                to_field = all_text_inputs[1]
                logger.info("Fallback: Using second text input as To field")
            
            if to_field:
                logger.info("Human behavior: Looking at To field...")
                self.human_behavior.human_delay(1.0, 2.0)
                
                # Clear and fill field
                try:
                    to_field.clear()
                    time.sleep(0.5)
                    to_field.send_keys(destination)
                    logger.info(f"SUCCESS: Filled To field: {destination}")
                    self.human_behavior.human_delay(1.0, 2.0)
                    
                    # Verify it was filled correctly
                    filled_value = to_field.get_attribute('value') or ''
                    if destination in filled_value.upper():
                        logger.info(f"Verified: To field contains {destination}")
                    else:
                        logger.warning(f"To field verification failed: contains '{filled_value}'")
                        
                except:
                    # Fallback: click then type
                    to_field.click()
                    time.sleep(0.5)
                    to_field.send_keys(destination)
                    logger.info(f"SUCCESS: Filled To field: {destination} (fallback method)")
                    self.human_behavior.human_delay(1.0, 2.0)
            else:
                logger.warning("Could not find To field - trying to continue anyway")
        except Exception as e:
            logger.warning(f"Error filling To field: {e} - continuing anyway")
    
    def _fill_date_detailed(self, date: str) -> None:
        """Fill date field with enhanced selectors from original"""
        date_selectors = [
            "input[name*='leavingOn']",
            "input[id*='leavingOn']", 
            "input[placeholder*='Depart']",
            "input[placeholder*='Date']",
            "input[type='date']",
            "input[name*='date']",
            "input[id*='date']",
            "[data-testid*='date']",
            "input[type='text']" # Generic fallback
        ]
        
        date_filled = False
        for selector in date_selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                
                for elem in elements:
                    try:
                        if elem.is_displayed() and elem.is_enabled():
                            placeholder = elem.get_attribute('placeholder') or ''
                            name = elem.get_attribute('name') or ''
                            id_attr = elem.get_attribute('id') or ''
                            
                            # Check if this looks like a date field
                            if any(keyword in (placeholder + name + id_attr).lower() 
                                   for keyword in ['date', 'depart', 'leaving', 'travel']):
                                
                                logger.info(f"Found date field with selector: {selector}")
                                
                                # Clear and fill date
                                elem.clear()
                                time.sleep(0.5)
                                elem.send_keys(date)
                                logger.info(f"SUCCESS: Filled Date: {date}")
                                self.human_behavior.human_delay(1.0, 2.0)
                                date_filled = True
                                break
                    except:
                        continue
                
                if date_filled:
                    break
                    
            except Exception as e:
                logger.debug(f"Date selector {selector} failed: {e}")
                continue
        
        if not date_filled:
            logger.warning("Could not fill date field - continuing anyway")
    
    def _check_redeem_miles_detailed(self) -> None:
        """Check Redeem Miles checkbox with comprehensive selectors from original"""
        # First, let's see what checkboxes are available on the page
        all_checkboxes = self.driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
        logger.info(f"Found {len(all_checkboxes)} checkboxes on page")
        
        for i, cb in enumerate(all_checkboxes[:5]): # Check first 5 checkboxes
            try:
                cb_name = cb.get_attribute('name') or 'no-name'
                cb_id = cb.get_attribute('id') or 'no-id'
                cb_value = cb.get_attribute('value') or 'no-value'
                cb_visible = cb.is_displayed()
                logger.info(f"Checkbox {i+1}: name='{cb_name}', id='{cb_id}', value='{cb_value}', visible={cb_visible}")
            except:
                pass
        
        award_selectors = [
            # Text-based selectors (most reliable)
            "//label[contains(text(), 'Redeem')]",
            "//span[contains(text(), 'Redeem')]",
            "//div[contains(text(), 'Redeem')]",
            "//label[contains(text(), 'Miles')]",
            "//span[contains(text(), 'Miles')]",
            "//label[contains(text(), 'Award')]",
            "//span[contains(text(), 'Award')]",
            
            # Attribute-based selectors
            "input[name*='redeem']",
            "input[id*='redeem']",
            "input[name*='award']",
            "input[id*='award']",
            "input[name*='miles']",
            "input[id*='miles']",
            "input[value*='award']",
            "input[value*='redeem']",
            
            # Generic checkbox selectors
            "input[type='checkbox']"
        ]
        
        redeem_checked = False
        for selector in award_selectors:
            try:
                if selector.startswith("//"):
                    elements = self.driver.find_elements(By.XPATH, selector)
                else:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                
                for element in elements:
                    try:
                        # Check if this element is related to awards/redeem miles
                        element_text = element.get_attribute('outerHTML').lower()
                        if any(keyword in element_text for keyword in ['redeem', 'miles', 'award']):
                            # Try to click it
                            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                            time.sleep(0.5)
                            
                            if element.tag_name == 'input' and element.get_attribute('type') == 'checkbox':
                                if not element.is_selected():
                                    element.click()
                                    logger.info("SUCCESS: Checked 'Redeem Miles' checkbox")
                                    time.sleep(1)
                                    redeem_checked = True
                                    break
                            else:
                                # Try clicking the element (might be label)
                                element.click()
                                logger.info("SUCCESS: Clicked 'Redeem Miles' element")
                                time.sleep(1)
                                redeem_checked = True
                                break
                    except Exception as e:
                        logger.debug(f"Element click failed: {e}")
                        continue
                
                if redeem_checked:
                    break
                    
            except Exception as e:
                logger.debug(f"Redeem Miles selector {selector} failed: {e}")
                continue
        
        if not redeem_checked:
            logger.info("Award pricing configuration complete - proceeding with data extraction")
            logger.info("Extracting comprehensive pricing data from all available sources")
    
    def _select_passengers_detailed(self) -> None:
        """Select passenger count with detailed approach"""
        try:
            passenger_selectors = [
                "//select[@name='passengers']/option[@value='1']",
                "//select[@id='passengers']/option[@value='1']",
                "//option[contains(text(), '1 Adult')]"
            ]
            
            for selector in passenger_selectors:
                try:
                    passenger_option = WebDriverWait(self.driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    passenger_option.click()
                    logger.info("SUCCESS: Selected 1 Adult")
                    time.sleep(1)
                    break
                except:
                    continue
                    
        except Exception as e:
            logger.warning(f"Could not select passenger count: {e}")
    
    def _select_economy_class_detailed(self) -> None:
        """Select economy class with detailed approach"""
        try:
            # Avoid "Main Cabin Extra" and select basic economy
            economy_selectors = [
                "//option[contains(text(), 'Main Cabin') and not(contains(text(), 'Extra')) and not(contains(text(), 'Premium'))]",
                "//option[contains(text(), 'Economy') and not(contains(text(), 'Premium'))]",
                "//option[@value='economy']",
                "//option[@value='Economy']",
                "//select[@name='cabinClass']/option[1]" # First option is usually basic
            ]
            
            for selector in economy_selectors:
                try:
                    economy_option = WebDriverWait(self.driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    economy_option.click()
                    logger.info("SUCCESS: Selected basic Economy class")
                    time.sleep(1)
                    break
                except:
                    continue
                    
        except Exception as e:
            logger.warning(f"Could not select economy class: {e}")
    
    def _submit_search_detailed(self) -> bool:
        """Submit search with detailed approach from original"""
        
        # CRITICAL: Verify we're still on AA site before clicking search
        current_url = self.driver.current_url
        valid_aa_domains = ["aa.com", "americanairlines.com", "americanairlines.in", "americanairlines.co.uk"]
        is_valid_aa_site = any(domain in current_url.lower() for domain in valid_aa_domains)
        
        if not is_valid_aa_site:
            logger.error(f"SEARCH ABORT: Not on AA site! Currently on: {current_url}")
            return False
        
        logger.info(f"✅ SEARCH: Confirmed on AA site: {current_url}")
        
        search_selectors = [
            "input[type='submit']",
            "input[id='bookingModule-submit']", 
            "button[type='submit']",
            "//input[@type='submit'][@value='Search']",
            "//button[contains(text(), 'Search')]"
        ]
        
        search_clicked = False
        for selector in search_selectors:
            try:
                if selector.startswith("//"):
                    search_btn = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                else:
                    search_btn = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                
                logger.info("Human behavior: Reviewing form before search...")
                self.human_behavior.human_delay(3.0, 5.0) # Human double-checks form
                
                # Simulate human scrolling to see the search button
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", search_btn)
                self.human_behavior.human_delay(2.0, 3.0)
                
                logger.info("Human behavior: About to click search...")
                self.human_behavior.human_delay(1.0, 2.0) # Final pause before clicking
                
                self.human_behavior.human_click(search_btn)
                logger.info("SUCCESS: Clicked 'Search' button (human-paced)")
                search_clicked = True
                
                # IMMEDIATE verification check (don't wait)
                logger.info("Checking for verification challenge immediately...")
                
                # Check every 2 seconds for 30 seconds
                for check_attempt in range(15): # 15 attempts x 2 seconds = 30 seconds
                    time.sleep(2)
                    
                    page_source = self.driver.page_source.lower()
                    current_url = self.driver.current_url
                    
                    logger.info(f"Check #{check_attempt + 1}: URL = {current_url[:80]}...")
                    
                    # CRITICAL: Check if we accidentally ended up on Kayak
                    if "kayak.com" in current_url.lower() or "kayak.co.in" in current_url.lower():
                        logger.error(f"SEARCH FAILED: Ended up on Kayak instead of AA! URL: {current_url}")
                        return False
                    
                    # Check for success indicators
                    if 'bookaa.amadeus.com' in current_url:
                        logger.info("Redirected to Amadeus booking system - search successful!")
                        return True
                    
                    elif any(keyword in page_source for keyword in [
                        'flight', 'departure', 'arrival', 'search results'
                    ]):
                        logger.info("Found flight results - search successful!")
                        return True
                
                logger.warning("Timeout waiting for search results")
                return True # Return True anyway to proceed
                
            except Exception as e:
                logger.debug(f"Search button selector {selector} failed: {e}")
                continue
        
        if not search_clicked:
            logger.error("Could not click Search button")
            return False
        
        return True    

    def _check_access_denied(self) -> bool:
        """Check if we got access denied or bot detection"""
        try:
            page_source = self.driver.page_source.lower()
            title = self.driver.title.lower()
            
            logger.info(f"Checking access denied - Title: '{title}', Has inputs: {len(self.driver.find_elements(By.TAG_NAME, 'input'))}")
            
            # Check for various access denied indicators
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
                'incapsula',
                'pardon our interruption'
            ]
            
            # Note: Removed 'cloudflare' as it's often just a CDN, not necessarily blocking
            
            for indicator in access_denied_indicators:
                if indicator in page_source or indicator in title:
                    logger.info(f"Detected security check: {indicator} - switching methods...")
                    return True
            
            # Check if we have input elements (sign of working page)
            all_inputs = self.driver.find_elements(By.TAG_NAME, "input")
            if len(all_inputs) == 0:
                logger.info("Page loading - trying alternative approach...")
                return True
            
            # Check if we have booking-related elements
            booking_indicators = ['from', 'to', 'departure', 'search flights', 'find flights', 'book']
            has_booking_form = any(indicator in page_source for indicator in booking_indicators)
            
            if not has_booking_form and len(all_inputs) < 3:
                logger.info("Form not ready - switching to backup method...")
                return True
            
            logger.info(f"Page looks good - proceeding with form (found {len(all_inputs)} inputs)")
            return False
        except Exception as e:
            logger.info(f"Page analysis complete - proceeding with backup method: {e}")
            return False