Questions
=========

.. code-block:: javascript

    //questions.js
    export const QuestionList = (props) => (
        <List {...props} title="Question List">
            <Datagrid>
                <TextField source="id"/>
                <TextField source="teacher.full_name"/>
                <TextField source="teacher.email"/>
                <TextField source="question_image"/>
                <TextField source="answer_image"/>
                <TextField source="choice"/>
                <TextField source="course"/>
                <TextField source="comment"/>
                <EditButton basePath="/questions"/>
                <DeleteButton basePath="/questions"/>
            </Datagrid>
        </List>
    );


    export const QuestionEdit = (props) => (
        <Edit {...props}>
            <SimpleForm>
                <DisabledInput source="id"/>
                <DisabledInput source="teacher.full_name"/>
                <TextInput source="teacher.email"/>
                <TextInput source="question_image"/>
                <TextInput source="answer_image"/>
                <TextInput source="choice"/>
                <TextInput source="course"/>
                <TextInput source="subject"/>
                <TextInput source="comment"/>
            </SimpleForm>
        </Edit>
    );

    export const QuestionCreate = (props) => (
        <Create title="Create a Question" {...props}>
            <SimpleForm>
                <TextInput source="teacher.email"/>
                <TextInput source="question_image"/>
                <TextInput source="answer_image"/>
                <TextInput source="choice"/>
                <TextInput source="course"/>
                <TextInput source="subject"/>
                <TextInput source="comment"/>
            </SimpleForm>
        </Create>
    );

    //app.js

        <Resource name="questions" list={QuestionList} edit={QuestionEdit} create={QuestionCreate} />


The code field given above describes question components. QuestionList, QuestionEdit and
QuestionCreate has necessary forms and fields. This views passed into Admin component in *App.js*.