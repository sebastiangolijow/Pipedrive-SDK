# SDK for Pipedrive

This SDK provides a Python interface to interact with Pipedrive, allowing control over various entities and operations within the Pipedrive CRM system. The SDK leverages Python, Pipedrive API, and libraries such as `enum` to provide a convenient and efficient way to manage Pipedrive entities.

## Models architecture

- The model architecture is the following:
  - Main abstract: This is the abstract for all entities and has all the main methods (get, all, filter, update, delete, etc.) **PipedriveAbstractModel/PipedriveFieldAbstractModel**
  - Abstract for entite: We have an abtract for each entite (Person, Organization, etc.) to set the url
  - Entitie mixin: inside each folder (investor/dealflow) we have a mixin with the api_key that will be use inside the abtract of the entitie inside the team folder
  - Abstract in team folder: we have 4 abstracts, this is cause it inherit the abstract for each entitie (Person, PersonField, Organization, OrganizationField) and its the base model for the actual entitie inside the team folder (BaseInvestorContactModel, BaseInvestorOrganizationModel, etc.)
  - Model: We have a model for each entitie defined inside each folder, this is cause we need a different contact model in investors or in dealflow, contact will have different fields in each folder cause it represent different things for each team. e.g: in investors: contact = user, organization = investor, dealflow: contact = user, organization = startup. PipedriveInvestorContact/PipedriveOrganizationContact.

## Features

* CRUD operations for Pipedrive entities.
* Special methods for managing custom fields in Pipedrive.
* Ability to create, update, retrieve, and delete entities.
* Easy integration with existing Python applications.

## Usage

To use the SDK, you need to initialize a model object based on the specific entity you want to interact with. For example, let's consider the `PipedriveContact` model:

 import PipedriveContact

person: PipedriveInvestorContact = PipedriveInvestorContact(id=1)

# Initialize a PipedriveContact object

person = PipedriveInvestorContact(id=1)

When initializing a `PipedriveContact` object, you can optionally provide the `id` parameter if you intend to perform operations that require searching for a specific person in the Pipedrive database (e.g: update, delete, etc).

### CRUD Operations

The SDK provides CRUD methods for managing Pipedrive entities. Here are some examples:

# Create a new person

new_person_data = {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "phone": "+1 123-456-7890"
}
new_person = PipedriveContact.create(new_person_data)

# Retrieve a person

person: PipedriveInvestorContact(id=1)

retrieved_person = person.get()

Initializate with an id then when executing the get method it will make a research for this id.

# Update a person

updated_person_data = {
    "email": "john.doe.updated@example.com"
}
updated_person = person.update(updated_person_data)

# Delete a person

person.delete()

**Custom Fields**

The SDK also provides methods for managing custom fields in Pipedrive. Here are some examples:

Create a custom field
new_field_data = {
    "name": "CustomField1",
    "field_type": "varchar"
}

personField: PersonField = PipedriveContactField()
new_field = person.add_custom_fields(new_field_data)

# Update a custom field

updated_field_data = {
    "name": "CustomField1Updated"
}
updated_field = person.update_custom_field(updated_field_data)

# Get all fields for a person

fields = person.get_all_fields()

These examples demonstrate how to perform various operations on Pipedrive entities using the SDK. You can explore the available methods for each entity model to access additional functionality.

# Note model

The note model is created to retrieve, update, delete and create notes inside an entitie that could be a deal/lead, person or organizartion.

This model is a bit different as the rest cause it only exists inside an entitie, we can't have a note that is not linked to a person, organization or deal/lead. Because of this we need to override some methods as the get method or the create method.

As this note can't be created without linked it to an entitie, the way that we create it changes too, we need to pass an id of the entity in the request now.

For the delete method, we need first, to get the notes of the entity that we want, search for the id of the note that we want to delete and then execute the delete method as usual. Same way as all the other entities.



# Activity model

The activity model is created to retrieve, update, delete and create activities. Activities are different of notes as an activity can exists by itself, without being linked with other entity as contact or organization

The methods works equal as the rest of the entities. We will have an all method to retrieve all activities, update to update an activity, create and get to get only one.

The only thing to take note here is the **type** field, this is the type of the activity and is an string, the value will come from the ActivityType entity.

We have an ActivityType entity also to get all activities, here we can search for the **key_string** of the ActivityType that we want to use and will be used as the **type** field in the creation or in the update of the activity.

Different of the option that have different keys/values/ids, the activityType key_string is not going to change, it is an string that is the same in every env. We can found a list of all activities with their key_strings inside the list.py file in utils folder in investor/dealflow folder

## Conclusion

The Pipedrive SDK provides a convenient way to interact with the Pipedrive CRM system using Python. With its support for CRUD operations, custom field management, and more.
