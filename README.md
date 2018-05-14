# KithAccountChecker
## Run using python 2.7

Checks if Kith accounts are valid.

## Instructions

  * First, you must enter all appropriate information in the **config** folder.
    * **Proxies.txt** is the name of the file you put your proxies in. (Refer to **Proxies**)
    * **Accounts.txt** is the name of the file you put your accounts in. (Refer to **Accounts**)
  * Secondly, you must install the modules required for the script to work. Please refer to **Required modules**.

## Proxies

  * Every proxy must be on its own line.
  * Every proxy must be the following format:

    * Supports IP Authentication proxies:
    ```ip:host```

    * Supports user:pass Authentication proxies:
    ```ip:host:user:pass```


  * **Example**:
  ```
  123.123.123.123:12345:hello:bye
  123.123.123.123:12345:hello:bye
  123.123.123.123:12345:hello:bye
  123.123.123.123:12345:hello:bye
  123.123.123.123:12345
  123.123.123.123:12345
  123.123.123.123:12345
  123.123.123.123:12345
  ```

## Accounts

  * Every account must be on its own line.
  * Every account must be the following format:
  ```email:password```


  * **Example**:
  ```
  terry@gmail.com:hello
  james@gmail.com:bye
  ```

## Required modules

Before running the script, the following modules are required:
```requests```

This can be accomplished by running the following command in a command prompt:

```
pip install requests
```

## Other scripts

I _might or might not_ release more scripts on my [twitter](https://twitter.com/zoegodterry).

Follow to be the **first ones to know**!
