DS Service

This service will be used to extract data from bank messages on User's Device.

This service will detect if the message recieved is related to the bank debit (expense) transaction or not.

If the message is related to the bank debit (expense) transaction, then it will extract the data from the message using llm model and send it to user-service through kafka.

User-Service will store the data in the database.