from behave import *
import json
from app import server

@given(u'the server is started')
def step_impl(context):
    context.app = server.app.test_client()
    context.server = server

@given(u'the following wishlists')
def step_impl(context):
    server.data_reset()
    for row in context.table:
        server.data_load_wishlist({"name": row['name'], "id": row['id'], "user_id": row['user_id']})

@given(u'the following items')
def step_impl(context):
    for row in context.table:
        server.data_load_wishlist_items({"id": row['item_id'], "wishlist_id": row['wishlist_id'], "description": row['description']})   

@when(u'I visit the "home page"')
def step_impl(context):
    context.resp = context.app.get('/')

@then(u'I should see "{message}"')
def step_impl(context, message):
    assert message in context.resp.data

@then(u'I should not see "{message}"')
def step_impl(context, message):
    assert message not in context.resp.data

@when(u'I visit "{url}"')
def step_impl(context, url):
    context.resp = context.app.get(url)
    assert context.resp.status_code == 200

@then(u'I should see a wishlist with id "{id}" and name "{name}"')
def step_impl(context, id, name):
    assert name and id in context.resp.data

@when(u'I delete "{url}" with id "{id}"')
def step_impl(context,url,id):
    target_url = '/{}/{}'.format(url, id)
    context.resp = context.app.delete(target_url)
    assert context.resp.status_code == 204
    assert context.resp.data is ""

@then(u'I should not see a wishlist with id "{id}" and name "{name}"')
def step_impl(context,id, name):
    assert name or id not in context.resp.data    

@when(u'I retrieve "{url}" with id "{id}"')
def step_impl(context, url, id):
    target_url = '/{}/{}'.format(url, id)
    context.resp = context.app.get(target_url)
    assert context.resp.status_code == 200

@then(u'I should see a wishlist with id "{id}"')
def step_impl(context, id):
    assert id in context.resp.data

@then(u'I should see "{message}" in this wishlist')
def step_impl(context, message):
    assert message in context.resp.data

@when(u'I change "{key}" to "{value}"')
def step_impl(context, key, value):
    data = json.loads(context.resp.data)
    data[key] = value
    context.resp.data = json.dumps(data)

@when(u'I update "{url}" with id "{id}"')
def step_impl(context, url, id):
    target_url = '/{}/{}'.format(url, id)
    context.resp = context.app.put(target_url, data=context.resp.data, content_type='application/json')
    assert context.resp.status_code == 200

@when(u'I delete an item with id "{item_id}" from wishlist with id "{wishlist_id}"')
def step_impl(context, item_id, wishlist_id):
    target_url = "wishlists/{}/items/{}".format(wishlist_id,item_id)
    context.resp = context.app.delete(target_url)
    assert context.resp.status_code == 204
    assert item_id not in context.resp.data

@then(u'I should not see an item with id "{id}" from wishlist with id "{wishlist_id}"')
def step_impl(context,id,wishlist_id):
    target_url = "wishlists/{}".format(wishlist_id)
    context.resp = context.app.get(target_url)
    assert id not in context.resp.data

@when(u'I update an item with id "{item_id}" in a wishlist with id "{wishlist_id}"')
def step_impl(context, item_id, wishlist_id):
    target_url = '/wishlists/{}/items/{}'.format(wishlist_id, item_id)
    context.resp = context.app.put(target_url, data=context.resp.data, content_type='application/json')
    assert context.resp.status_code == 200

@when(u'I create new wishlist at "{url}" with user_id "{user_id}" and name "{wishlist_name}"')
def step_impl(context,url,user_id,wishlist_name):
    data = {"name":wishlist_name,"user_id":user_id}
    context.resp = context.app.post(url, data=json.dumps(data), content_type='application/json')
    assert context.resp.status_code == 201

@when(u'I create an item with id "{item_id}" and description "{message}" to wishlist id "{wishlist_id}"')
def step_impl(context,item_id,message,wishlist_id):
    data = {"id":item_id,"description":message}
    url = "wishlists/{}/items".format(wishlist_id)
    context.resp = context.app.post(url, data=json.dumps(data), content_type='application/json')
    assert context.resp.status_code == 201

@when(u'I retrieve an item with id "{item_id}" from wishlist id "{wishlist_id}"')
def step_impl(context,item_id,wishlist_id):
    target_url = "wishlists/{}/items/{}".format(wishlist_id, item_id)
    context.resp = context.app.get(target_url)
    assert context.resp.status_code == 200

@then('I should see an item with id "{item_id}" and description "{message}"')
def step_impl(context,item_id,message):
    assert item_id in context.resp.data and message in context.resp.data

@when('I search for query "{q}" in all wishlists with user id "{uid}"')
def step_impl(context,q,uid):
    target_url = "wishlists/search?q={}&user_id={}".format(q, uid)
    context.resp = context.app.get(target_url)
    assert context.resp.status_code == 200

