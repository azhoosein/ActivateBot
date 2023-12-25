from objects import Logins
import pyautogui
from db import establish_connection

screenWidth, screenHeight = pyautogui.size()
currentMouseX, currentMouseY = pyautogui.position()

coordinates = {
    'CbTM10_TT1Kw1Xc_1mo-0': (463, 495),
    'CbTM15_TTUw3.5Xc_1mo': (463, 595),
    'CbTM25_TTUw6.5Xc_1mo': (463, 695),
    'CbTM35_TTUw12Xc_1mo': (463, 795),
    'TPP50TTUwULX': (463, 495),
    'TPP60TTUwULXPLUS': (463, 595),
    'TPP40TTUw10X': (463, 695)
}

def getLogins(connection):
    login_query = "SELECT id, tmobile_user, tmobile_password, epay_user, epay_password FROM logins WHERE state = 'active' AND id=1 AND balance > 30 ORDER BY RAND() LIMIT 1"
    try:
        with connection.cursor() as cursor:
            cursor.execute(login_query)
            login_data = cursor.fetchone()

            if login_data:
                login = Logins(*login_data)
                print("----------Login Retrieved----------")
                return login
            else:
                print("Login Not Found")
    except Exception as e:
        print("Error:", str(e))

    
def failActivation(message, activation, connection):
    # SQL query to update status and comments for a specific activation_id
    fail_query = "UPDATE tmobile_activation SET status = 'Failed', comments = %s WHERE activation_id = %s"
    try:
        connection = establish_connection()
        with connection.cursor() as cursor:
            # Execute the SQL query with activation_id and comments as parameters
            cursor.execute(fail_query, (message, activation.activation_id))
            # Commit the changes to the database
            connection.commit()
        print("Activation status and comments updated successfully.")
    except Exception as e:
        # Handle exceptions that might occur during the database operation
        default_comment = "Activation Failed due to an internal error."
        print(f"Error updating activation status and comments: {e}")
        # Retry updating the activation status and set a default comment in case of another exception
        try:
            with connection.cursor() as cursor:
                cursor.execute(fail_query, (default_comment, activation.activation_id))
                connection.commit()
            print("Activation status and comments set to default due to an error.")
        except Exception as retry_error:
            print(f"Error setting default activation status and comments: {retry_error}")

def CompleteActivation(activation, connection, Number, ACCT_NUMBER, RECIEPT, PIN):
    # SQL query to update status and comments for a specific activation_id
    Completion_query = "UPDATE tmobile_activation SET status = 'Complete;, phone = %s, account_number = %s, receipt = %s, pin = %s WHERE activation_id = %s"
    try:
        connection = establish_connection()
        with connection.cursor() as cursor:
            # Execute the SQL query with activation_id and comments as parameters
            cursor.execute(Completion_query, (Number, activation.activation_id))
            # Commit the changes to the database
            connection.commit()
        print("Activation status and comments updated successfully.")
    except Exception as e:
        print(f"Error updating activation status and comments: {e}")

    
def selectPlan(activation, driver):
    pyautogui.scroll(-750)
    if "TPP" in activation.plan_name:
        if driver.is_element_visible("#ui-tabpanel-1-label"):
            driver.sleep(1)
            driver.click("#ui-tabpanel-1-label")
            driver.sleep(1)
            try:
                if activation.plan_name in coordinates:
                    x, y = coordinates[activation.plan_name]
                    pyautogui.moveTo(x, y)
                    driver.sleep(1)
                    pyautogui.click()
                    print("PLAN CLICKED")
                    driver.sleep(2)
                    return True
            except Exception as e:
                print("Error Selecting Plan")
                return False            
        else:
            return False
    elif "CbTM" in activation.plan_name:
        if driver.is_element_visible("#ui-tabpanel-0-label"):
            driver.sleep(2)
            try:
                if activation.plan_name in coordinates:
                    x, y = coordinates[activation.plan_name]
                    pyautogui.moveTo(x, y)
                    driver.sleep(1)
                    pyautogui.click()
                    print("PLAN CLICKED")
                    driver.sleep(1)
                    return True
            except Exception as e:
                print("Error Selecting Plan")
                return False
        else:
            return False
        
def selectAddon(activation, driver):
    if activation.addon_name != "no_addon":
        if driver.is_element_visible("#ui-tabpanel-7-label"):
            driver.sleep(1)
            driver.click("#ui-tabpanel-7-label")
            driver.sleep(2)
            if activation.selected_addon == "($5.00) Mexico & Canada Unlimited - $1.25" and driver.is_element_visible("/html/body/main/div[9]/tmo-root/div/main/tmo-repdash/div/div/div/tmo-rap-home/div/div[3]/p-accordion/div/p-accordiontab[3]/div[2]/div/tmo-rap-manage-services/div[2]/p-tabview/div/div/p-tabpanel[2]/div/div[2]/div[1]/tmo-checkbox/label/span/input"):
                driver.click("/html/body/main/div[9]/tmo-root/div/main/tmo-repdash/div/div/div/tmo-rap-home/div/div[3]/p-accordion/div/p-accordiontab[3]/div[2]/div/tmo-rap-manage-services/div[2]/p-tabview/div/div/p-tabpanel[2]/div/div[2]/div[1]/tmo-checkbox/label/span/input")
                return True
            else:
                return False
            
