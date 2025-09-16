from pydantic import BaseModel, Field, SecretStr, field_validator

class RedisConfig(BaseModel):
    host: str = 'localhost'
    port: int = 6379
    username: str = 'default'
    password: SecretStr 
    db: int = 0
    ssl: bool = True
    connection_timeout: int = 10
    
    @field_validator('port', 'db', 'connection_timeout', mode='before')
    @classmethod
    def convert_string_to_int(cls, v):
        if isinstance(v, str):
            # Handle environment variable placeholders
            if v.startswith('${') and v.endswith('}'):
                # Return default values for missing environment variables
                if 'REDIS_PORT' in v:
                    return 6379
                elif 'REDIS_DB' in v:
                    return 0
                elif 'connection_timeout' in v:
                    return 10
            return int(v)
        return v
    
    @field_validator('ssl', mode='before')
    @classmethod
    def convert_string_to_bool(cls, v):
        if isinstance(v, str):
            # Handle environment variable placeholders
            if v.startswith('${') and v.endswith('}'):
                if 'REDIS_SSL' in v:
                    return False
            return v.lower() in ('true', '1', 'yes', 'on')
        return v
    
    @field_validator('password', mode='before')
    @classmethod
    def convert_string_to_secret(cls, v):
        if isinstance(v, str):
            # Handle environment variable placeholders
            if v.startswith('${') and v.endswith('}'):
                if 'REDIS_PASSWORD' in v:
                    return ""
            return v
        return v