# Import necessary libraries and modules
from seleniumbase import Driver
import time
import pyautogui
from db import establish_connection
from objects import Activation, Logins
from helpers import getLogins, failActivation, CompleteActivation, selectPlan, selectAddon

# Define a function to open T-Mobile portal and return the driver object
def open_tmobile_portal(login):
    driver = Driver(uc=True)
    driver.open("chrome://newtab")
    driver.sleep(2)
    driver.get("https://beta.rap.t-mobile.com/rap")
    driver.wait_for_element("#okta-signin-username")
    driver.type("#okta-signin-username", login.tmobile_user)
    driver.sleep(1)
    driver.type("#okta-signin-password", login.tmobile_password)
    driver.sleep(1)
    driver.click("#okta-signin-submit")
    driver.sleep(1)
    driver.maximize_window()
    pyautogui.moveTo(507, 802)
    return driver

# Define a function to enter ZIP code during activation
def enter_zip_code(driver, activation):
    try:
        driver.wait_for_element("#tmo-input-default-118")
        driver.sleep(2)
        driver.type("#tmo-input-default-118", activation.zip_code)
        return True
    except Exception as e:
        print("SITE NOT LOADING")
        return False

# Define a function to enter IMEI number during activation
def enter_imei(driver, activation):
    try:
        driver.wait_for_element("#tmo-input-default-74")
        driver.sleep(1)
        driver.type("#tmo-input-default-74", activation.imei_number)
        driver.sleep(2)
        return True
    except Exception as e:
        print("INVALID IMEI")
        return False

# Define a function to check compatibility during activation
def check_compatibility(driver):
    try:
        driver.click("#checkCompatibility")
        driver.sleep(2)
        if driver.is_element_visible("#errorMessage0"):
            errorMsg = driver.get_text("#errorMessage0")
            print(errorMsg)
            return False, errorMsg
        return True, ""
    except Exception as e:
        print("INVALID IMEI")
        return False, "INVALID IMEI"

# Define a function to enter SIM card information during activation
def enter_sim(driver, activation):
    try:
        driver.wait_for_element("#tmo-input-default-76")
        driver.sleep(1)
        driver.type("#tmo-input-default-76", activation.sim_eid)
        driver.sleep(2)
        return True
    except Exception as e:
        print("INVALID SIM")
        return False

# Define a function to validate SIM card during activation
def validate_sim(driver):
    try:
        driver.click("#checkSimValidationButton")
        driver.sleep(2)
        if driver.is_element_visible("#errorMessage0"):
            errorMsg = driver.get_text("#errorMessage0")
            print(errorMsg)
            return False, errorMsg
        return True, ""
    except Exception as e:
        print("INVALID SIM")
        return False, "INVALID SIM"

# Define a function to select a plan during activation
def select_plan(driver, activation):
    try:
        if selectPlan(activation, driver):
            print(f"Plan Selected: {activation.selected_plan}")
            return True, ""
        else:
            errorMsg = "Plan Not Found"
            return False
    except Exception as E:
        print("Plan Not Found")
        return False, "Plan Not Found"

# Define a function to select an addon during activation
def select_addon(driver, activation):
    try:
        if activation.addon_name != "no_addon":
            addonSelected = selectAddon(activation, driver)
            if addonSelected:
                print(f"Addon Selected: {activation.selected_addon}")
                return True, ""
            else:
                errorMsg = "Plan Not Found"
                return False, ""
        else:
            return True, ""
    except Exception as e:
        print("Addon Not Found")
        return False, "Addon Error"

# Define a function to handle plan selection during activation
def handle_plan_selection(driver):
    try:
        if driver.is_element_visible("#continueToStepFourButton"):
            driver.sleep(10)
            driver.click("#continueToStepFourButton")
            driver.sleep(2)
            if driver.is_element_visible("#errorMessage0"):
                errorMsg = driver.get_text("#errorMessage0")
                print(errorMsg)
                return False, "INVALID PLAN SELECTION"
            else:
                return True, ""
        else:
            print("INVALID PLAN SELECTION")
            return False, "INVALID PLAN SELECTION"
    except Exception as e:
        print("INVALID PLAN SELECTION")
        return False, "INVALID PLAN SELECTION"

# Define a function to retrieve the phone number during activation
def retrieve_phone_number(driver, activation):
    try:
        driver.wait_for_element("#cta-default-116")
        driver.sleep(1)
        driver.type("#cta-default-116", activation.zip_code)
        driver.sleep(1)
        pyautogui.moveTo(867, 305)
        driver.sleep(1)
        pyautogui.click()
        driver.sleep(1)
        if driver.is_element_visible("#errorMessage0"):
            errorMsg = driver.get_text("#errorMessage0")
            print(errorMsg)
            return False, 1, "Number Could Not Be Retrieved"
        driver.wait_for_element("#reserve-msisdn-line")
        Number = driver.get_text("#reserve-msisdn-line")
        return True, Number, ""
    except Exception as E:
        print("Number Could Not Be Retrieved")
        return False, 1, "Number Could Not Be Retrieved"

# Define a function to complete line setup during activation
def complete_line_setup(driver):
    try:
        if driver.is_element_visible("#button-on-complete-line-setup"):
            driver.sleep(1)
            driver.click("#button-on-complete-line-setup")
            if driver.is_element_visible("#errorMessage0"):
                errorMsg = driver.get_text("#errorMessage0")
                print(errorMsg)
                return False, errorMsg
            driver.sleep(2)
            driver.click("#button-on-continue")
            if driver.is_element_visible("#errorMessage0"):
                errorMsg = driver.get_text("#errorMessage0")
                print(errorMsg)
                return False, errorMsg
            return True, ""
    except Exception as e:
        print("Error completing line setup:", str(e))
        return False, "Error completing line setup"

# Define a function to enter PIN during activation
def enter_pin(driver, pin):
    try:
        pin_str = str(pin)
        driver.wait_for_element("#tmo-input-default-94")
        driver.sleep(1)
        driver.type("#tmo-input-default-94", pin_str)
        driver.sleep(1)
        driver.type("#tmo-input-default-95", pin_str)
        driver.sleep(2)
        driver.click("#backToTop")
        if driver.is_element_visible("#errorMessage0"):
            errorMsg = driver.get_text("#errorMessage0")
            return False, errorMsg
        return True, ""
    except Exception as e:
        print("ERROR HAPPENING IN PIN AREA")
        print(e)
        return False, e

# Define a function to login to Epay during activation
def login_epay(driver, login):
    try:
        driver.sleep(1)
        driver.wait_for_element("#inputEmail")
        driver.sleep(1)
        driver.type("#inputEmail", login.epay_user)
        driver.sleep(1)
        driver.type("#inputPassword", login.epay_password)
        pyautogui.moveTo(942, 311)
        driver.sleep(1)
        pyautogui.click()
        driver.sleep(8)
        return True, ""
    except Exception as e:
        print("ERROR HAPPENING IN LOGIN EPAY AREA")
        print(e)
        return False, "Error Logging Into Epay"

# Define a function to submit activation during activation
def submit_activation(driver):
    try:
        driver.wait_for_element("#submitTransaction")
        driver.sleep(10)
        driver.click("#submitTransaction")
        driver.sleep(10)
        if "https://beta.rap.t-mobile.com/rap/order-confirmation" in driver.get_current_url():
            return True, ""
    except Exception as e:
        print("ERROR HAPPENING IN SUBMIT ACTIVATION AREA")
        print(e)
        return False, "Error Submiting Transaction"

# Define a function to complete the entire activation process
def complete_activation_process(activation, login, cursor, connection):
    driver = open_tmobile_portal(login)
    if not driver:
        activationErrorMsg = "Failed to load tmobile portal"
        failActivation(activationErrorMsg, activation, connection)
        return
    
    if not enter_zip_code(driver, activation):
        activationErrorMsg = "SITE NOT LOADING"
        failActivation(activationErrorMsg, activation, connection)
        driver.quit()
        return
    
    if not enter_imei(driver, activation):
        activationErrorMsg = "INVALID IMEI"
        failActivation(activationErrorMsg, activation, connection)
        driver.quit()
        return
    
    compatible, errorMsg = check_compatibility(driver)
    if not compatible:
        failActivation(errorMsg, activation, connection)
        driver.quit()
        return
    
    if not enter_sim(driver, activation):
        activationErrorMsg = "INVALID SIM"
        failActivation(activationErrorMsg, activation, connection)
        driver.quit()
        return
    
    sim_validated, errorMsg = validate_sim(driver)
    if not sim_validated:
        failActivation(errorMsg, activation, connection)
        driver.quit()
        return
    
    plan_selection, errorMsg = select_plan(driver, activation)
    if not plan_selection:
        failActivation(errorMsg, activation, connection)
        driver.quit()
        return

    addon_selection, errorMsg = select_addon(driver, activation)
    if not addon_selection:
        failActivation(errorMsg, activation, connection)
        driver.quit()
        return
    
    plan_submit, errorMsg = handle_plan_selection(driver)
    if not plan_submit:
        failActivation(errorMsg, activation, connection)
        driver.quit()
        return
    
    number_retrieved, Number, errorMsg = retrieve_phone_number(driver, activation)
    if not number_retrieved:
        failActivation(errorMsg, activation, connection)
        driver.quit()
        return
    
    complete_line_setup_success, errorMsg = complete_line_setup(driver)
    if not complete_line_setup_success:
        failActivation(errorMsg, activation, connection)
        driver.quit()
        return
    
    pin_entered, errorMsg = enter_pin(driver, 101010)
    if not pin_entered:
        failActivation(errorMsg, activation, connection)
        driver.quit()
        return

    epay_loggedIn, errorMsg = login_epay(driver, login)
    if not epay_loggedIn:
        failActivation(errorMsg, activation, connection)
        driver.quit()
        return
    
    activation_submited, errorMsg = submit_activation(driver)
    if not activation_submited:
        failActivation(errorMsg, activation, connection)
        driver.quit()
        return
    
    CompleteActivation(activation, connection, Number, "pending", "pending", 101010)
    driver.quit()
    return

# Define a function to check and complete activation
def check_and_complete_activation():
    try:
        # Establish a database connection
        connection = establish_connection()
        with connection.cursor() as cursor:
            # Query for retrieving a new activation
            activation_query = """
            SELECT activation_id, imei_number, sim_eid, plan_name, status, zip_code, addon_name, sim_type, requestor_id, firstname, lastname, email, amount, selected_plan, selected_addon
            FROM tmobile_activation 
            WHERE status = 'New'
            LIMIT 1;
            """
            cursor.execute(activation_query)
            activation_data = cursor.fetchone()

            if activation_data:
                activation = Activation(*activation_data)
                login = getLogins(connection)
                if activation and login:
                    print("----------Activation Data Retrieved----------")
                    # Update activation status to 'Processing'
                    update_query = "UPDATE tmobile_activation SET status = 'Processing' WHERE activation_id = %s"
                    cursor.execute(update_query, (activation.activation_id,))
                    connection.commit()
                    print(activation)
                    complete_activation_process(activation, login, cursor, connection)
                else:
                    print("Error Retrieving Login Data or Activation Data")
            else:
                print("No new activation found")
    except Exception as e:
        print(f"Error: {e}")

# Run the activation check and completion in an infinite loop with a sleep interval
while True:
    check_and_complete_activation()
    time.sleep(20)
