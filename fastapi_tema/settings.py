""" settings """


from pydantic import BaseSettings 

class Settings_my(BaseSettings):
    """_summary_

    Args:
        BaseSettings (_type_): _description_
    """
    main_url: str = "/"
    
    
settings = Settings_my()