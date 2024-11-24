import re 
import logging
logger = logging.getLogger(__name__)


def credits_by_message(message):
    #Base Cost: Every message has a base cost of 1 credit.
    cost = 1

    #Character Count: Add 0.05 credits for each character in the message.
    cost += ( len(message) * 0.05 )
    logger.debug('Add 0.05 per character. Characters:%s Cost:%s', len(message), cost)

    unique_words = []
    all_unique_words = True
    #(Note: A “word” is defined as any continual sequence of letters, plus ' and -)
    for word in re.findall( "[a-zA-Z-']+", message ) : #This regex finds every word using that specification. + indicates the word must be at least length 1.
        
        ###**Word Length Multipliers:**
        ###- For words of 1-3 characters: Add 0.1 credits per word.
        ###- For words of 4-7 characters: Add 0.2 credits per word.
        ###- For words of 8+ characters: Add 0.3 credits per word.
        #Now we know we have a word, it's just a case of adding the correct cost for it
        wordlength = len(word)
        if ( wordlength < 4 ):
            cost += 0.1
            logger.debug('Word "%s" is length 1-3, add 0.1 Cost:%s', word, cost)
        elif ( wordlength < 8 ):
            cost += 0.2
            logger.debug('Word "%s" is length 4-7, add 0.2 Cost:%s', word, cost)
        else:
            cost += 0.3
            logger.debug('Word "%s" is length 8+, add 0.3 Cost:%s', word, cost)

        ###Unique Word Bonus: If all words in the message are unique (case-sensitive), subtract 2 credits from the total cost (remember the minimum cost should still be 1 credit).
        if all_unique_words :   #If there's still a possibility that all words are unique
            if ( word in unique_words ):  #If this word is in the list of unique words collected so far
                all_unique_words = False  #Then there is no longer the possibility that all words are unique, set flag false
                logger.debug('Not all words are unique, no bonus this time. More than one "%s" found.', word )
            else: # this word is not already in the list of unique words
                unique_words.append( word )  #so add it and keep looking
    
    #Comming out of our word loop, if we found that all the words were unique then there's a bonus to be applied
    if all_unique_words :
        cost -= 2
        logger.debug('Every word is unique! Subtract 2 from cost as a bonus. Cost:%s', cost)
    
    ###Third Vowels: If any third (i.e. 3rd, 6th, 9th) character is an uppercase or lowercase vowel (a, e, i, o, u) add 0.3 credits for each occurrence.
    #Use slicing to create a new string that is every third character in the message starting at the third character (index 2)
    every_third = message[2::3]
    logger.debug('Every third character is "%s"', every_third)
    #Then use regex to pull out the vowels
    for vowel in re.findall( '[aeiou]', every_third, re.IGNORECASE):
        cost += 0.3
        logger.debug('Found vowel "%s" as a third character, add 0.3. Cost:%s', vowel, cost)

        
    ###Length Penalty: If the message length exceeds 100 characters, add a penalty of 5 credits.
    if ( len(message) > 100 ):
        cost += 5
        logger.debug('Message length is greater than 100, add 5. Cost:%s', cost)
    

    #(remember the minimum cost should still be 1 credit).   - prior to palindrome doubling 
    if ( cost < 1 ):
        cost = 1
        logger.debug('After rules were applied the cost was less than base cost. Cost reset to base. Cost:%s', cost )


    #Palindromes: If the entire message is a palindrome (that is to say, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward), double the total cost after all other rules have been applied.
    lower_alpha = re.sub( r'[^a-z0-9]+', '', message.lower() )    #only alpha nemeric characters.  (can't use \w as that has _)
    if ( lower_alpha == lower_alpha[::-1] ):  #if alpha numeric only matches itself reversed, then it's a palindrome.
        cost = cost * 2
        logger.debug('Palindrome detected, cost doubled! "%s" is the same backwards. Cost:%s', lower_alpha, cost )
    else:
        logger.debug('Not a palindrome: "%s"', lower_alpha )

    cost = round(cost, 2)  #Maths is not python's strongest point. Given we have only ever dealt with 2dps, let's get back to that and shed any extra decimals
    logger.info('Final cost: %s For text: %s', cost, message)
    return cost


def tests():
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    credits_by_message('WhAt is the security deposit?')  #Cost 2.55
    credits_by_message('WhAt is @the secu!rity Deposit tisoped ytiruces eht si tAhW')   #Cost 13.10
