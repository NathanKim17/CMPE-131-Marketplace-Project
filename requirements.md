## Functional Requirements

1. User Login
2. User Logout
3. Create new user account
4. Delete account
5. Change your password
6. Add items to shopping cart
7. Remove Items from cart
8. Enter coupon code
9. Searching Items (by name or ID Number)
10. Adding a user review for a product
11. Update payment option
12. Password Recovery (via email verification)

## Non-functional Requirements

1. Only expected to run on Google Chrome.
2. The website will have an intuitive layout (easy for the user to maneuver).
3. The website will be available to the user twenty-four hours a day (seven days a week).
4. The website will only sanction safe, reliable, and valid transactions.

## Use Cases

### 1. Adding a user review for a product
  Pre-condition: The user must have an account and they must be logged in.

  Trigger: The user clicks the "Add Review" button after writing a review.

  Primary Sequence:
  
  1. User is viewing a particular product and clicks the "Add Review" button
  2. The user writes a short review about the product.
  3. The user selects how many stars (out of five) they would rate the product.
  4. The user clicks the "Add Review" button.

  Primary Postconditions: The user will see a confirmation message confirming that their review has been saved.

### 2. Change your password
  Pre-condition: The user must have an account, be logged in, and have an existing password. The user must also currently be on the "Account" page.
  
  Trigger: Select the "Enter" option.
  
  Primary Sequence:
   1. The user must navigate to their "Account Details" (click "Account Details" option).
   2. Select the "Change Password" option.
   3. User is presented an input box where they will enter their old password.
   4. If the old password matches, the page will direct the user to an input box where they will enter their new password.
   5. User selects the "Enter" button to confirm.

  Alternate Sequence:
   1. If the user enters the old password as the new password, then there will be an error message. 
   2. Prompt the user to re-enter the old password and new password. 
    
   Primary Postconditions: The user will be redirected back to the home page where they will be greeted with a confirmation flash message confirming that their password was successfully updated.

### 3. Add items to shopping cart
  Pre-condition: The user must have an account and they must be logged in.
  
  Trigger: Select the "Add to Shopping Cart" button.
  
  Primary Sequence:
   1. The user must navigate to their "Browse Items" section of the website.
   2. The user must view the details of a particular product (by selecting the "View Details" option associated with that product).
   3. User must select the "Add to Shopping Cart" option.
    
   Primary Postconditions: The user will see the item added to their shopping list.
   
### 4. Remove items from cart
  Pre-condition: The user must have an account and they must be logged in. The shopping cart must have at least one item in it.
  
  Trigger: User clicks the "Remove Item" button associated with a particular product in their shopping cart.
  
  Primary Sequence:
   1. The user must navigate to the "Shopping Cart" menu.
   2. The user clicks on the "Remove Item" button associated with the product they wish to remove from their shopping cart.
   
   Primary Postcondition: The page refreshes and the user is presented a confirmation message and the item is deleted from the shopping cart.
  
### 5. Searching Items (by name or ID Number)
  Pre-condition: Website must be running on Google Chrome and the user must have access to the website.
  
  Trigger: User presses the return key after entering the search criteria.
  
  Primary Sequence:
   1. The user navigates to the "Browse Items" page.
   2. The user user enters the name or ID numbers into the appropriate text box (there will be one textbox for names and one for ID numbers).
    
   Primary Postcondition: The page will refresh with the results of the search (most relevant items).
  
### 6. Update payment option
  Pre-condition: The user must have an account and they must be logged in.
  
  Trigger: The user clicks the "Save" Button
  
  Primary Sequence:
   1. The user must navigate to their "Account Details" (click "Account Details" option).
   2. Select the "Update Payment" button.
   3. Prompt the user to enter a new Credit/Debit information.
   4. The user clicks on the "Save".

  Alternate Sequence:
   1. If the user enters an invalid input, then there will be an error message.
   2. Prompt the user to re-enter card information.
    
   Primary Postcondition: The page refreshes and the user will see the updated payment information.
