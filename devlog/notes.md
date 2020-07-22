# Developer Log

I've decided to begin taking notes concerning my dev experience. I will treat this log as though I were speaking to it but slightly more professional and educational than my usual tone. 

## July 15, 2020 
---
<a id="iss1"></a>

#### 71dd13136681af3669f4dfdc38150b043ac2cf5f

`Tags: Server, Frontend, CORS, Fetch`


I have successfully implemented cookies on the front and backend. I was having trouble with the fetch api and specifically, CORS. I learned a couple things:

1. For CORS requests, Fetch requires `credentials: include` in order to set and recieve cookies
2. For CORS requests to succeed, `Access-Allow-Origin` cannot be the wildcard, `*`



From here I am facing a new issue, [Issue #1](#iss1)


```
Cookie “clastic_cookie” will be soon rejected because it has the “sameSite” attribute set to “none” or an invalid value, without the “secure” attribute. 
To know more about the “sameSite“ attribute, read https://developer.mozilla.org/docs/Web/HTTP/Headers/Set-Cookie/SameSite
```
----
#### fddb7947576a66ad01b46fcc17dac73b5c92e7fe

`Tags: Game Engine, Interpolation, Custom Piece`

I fixed an issue with the interpolation functions that caused it to straight up not work. I also generalized the move function to allow custom interpolators per piece! This will be handy later on when I want to design custom pieces

----
## July 19, 2020

### e0ff19102ea8d454dab4e94dc909cad2c4a5475f

`Tags: Middleware, Clastic, Router`

I created a middleware to unpack post request data and feed it to my functions. 

<a id="iss1"></a>

At the moment there is no way of automatically define which function parameters should be unpacked from the request so they are currently *defined manually*, I'll be calling this [Issue#2](#iss2). This doesn't involve a significant burden.

This method does come with 2 drawbacks:

 1. leaves room for mistakes 
 2. tightly couples the function definition to the route definition. 

I have 1 potential solution for Issue#2 and 1 more half baked thought

1.  Using the function signature and param names as an internal code

```
#an example in pseudocode

def func_foo(a, unpack_b, unpack_c):
  ...

class Unpack(Middleware):
  def __init__(foo: function):
    provides = filter foo.params with prefix unpack_
  
```
** remember: `provides` tells clastic that what this middleware will pass into the next function **

With this, the function arguments could be adjusted at any time without needing to edit the `Unpack` instance declaration

2. Using decorators in some way

<a id="iss3"></a>

Currently, defining new routes is cumbersome. I'll call this [Issue 3](#iss3)

---

## July 21, 2020

I have a problem to solve here. When a user is using the site, they have certain data associated with their session. Like board game information. The user is often going to need this. However, this information must be secure and only available to a validated user. 

---
#### How do you know if a user is valid?

<a id='feature1'></a>
A user will post a login request with the shape `{username, password}`
that request will be validated and on success will return a **secure cookie** containing at least `userid`

on any subsequent secure request the **secure cookie** will be decrypted and a valid `user_id` will signify a valid user. I'll call this [feature 1](#feature1)



Some more information might be required, such as

1. session_id
2. device information
3. expire_date
4. persistant 

It might be a good idea to transition this to a *JWT*. I may comment on that in the future.

---
#### on the subject of endpoints and aggegating user_session info into a single request

it may be the case that a user needs many bits of information available at many endpoints. using `REST` endpoints might make it difficult to request different shapes of data; `Graphql` solves this problem but seems lilke a giant to tackle my relatively small problem. Instead, I am thinking about using a special endpoint that instead redirects data to it's various endpoints

Here's what I mean, keep in mind the shape of the data is purely for demonstration and `{key}` corresponds to `{key: value}` but omits the value for simplicity


```
#lets imagine we have endpoints /foo and /bar that call their respective functions `foo` and `bar`

def foo(a,b):
  pass

def bar(b,c,d):
  pass

```
1. the users sends some data to /generic: `{data:{a,b,c,d}, endpoints:[foo,bar]}`
2. /generic redirects `data` to the move endpoint
3. `Unpack` middleware unpacks the relevant data (in this case `a` and `b`) and calls move
4. /generic captures its response 
5. repeat step 3 and 4 until all endpoints have been called
6. send response in shape {move, sync}


interestingly, step 3 happens for free because `Unpack` is defined on the endpoints themselves

<a id='note1'></a>

#### [note 1](#note1)
 
Programmers in dynamic languages have a tendency to shove tons of functionality into single functions. That might have something to do with oop backgrounds. Try to avoid that


---

#### How does the server provide user information to functions?

I'm going to pick the example of the `/move` endpoint. 

When a user submits a move they also must submit 3 pieces of information
1. user id (1 per user)
2. board id (>0 per user)
3. the move


