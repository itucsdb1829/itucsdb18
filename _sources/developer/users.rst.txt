Users
=====

.. code-block:: javascript

    //users.js
    export const UserList = (props) => (
        <List {...props} title="User List">
            <Datagrid>
                <TextField source="id"/>
                <TextField source="name"/>
                <TextField source="surname"/>
                <TextField source="email"/>
                <TextField source="phone_number"/>
                <TextField source="role"/>
                <TextField source="iban"/>
                <EditButton basePath="/users"/>
                <DeleteButton basePath="/users"/>
            </Datagrid>
        </List>
    );

    const UserTitle = ({record}) => {
        return <span>User {record ? `"${record.name}"` : ''}</span>;
    };

    export const UserEdit = (props) => (
        <Edit title={<UserTitle/>} {...props}>
            <SimpleForm>
                <DisabledInput source="id"/>
                <TextInput source="name"/>
                <TextInput source="surname"/>
                <TextInput source="email"/>
                <TextInput source="phone_number"/>
                <TextInput source="role"/>
                <TextInput source="iban"/>
            </SimpleForm>
        </Edit>
    );

    export const UserCreate = (props) => (
        <Create title="Create an User" {...props}>
            <SimpleForm>
                <TextInput source="name"/>
                <TextInput source="surname"/>
                <TextInput source="password"/>
                <TextInput source="email"/>
                <TextInput source="phone_number"/>
                <TextInput source="role"/>
                <TextInput source="iban"/>
            </SimpleForm>
        </Create>
    );

    //app.js

       <Resource name="users" list={UserList} edit={UserEdit} create={UserCreate} />


The code field given above describes user components. UserList, UserEdit and
UserCreate has necessary forms and fields. This views passed into Admin component in *App.js*.