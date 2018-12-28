Feedbacks
=========

.. code-block:: javascript

    //feedbacks.js
    export const FeedbackList = (props) => (
        <List {...props} title="User List">
            <Datagrid>
                <TextField source="id"/>
                <TextField source="reviewer.full_name"/>
                <TextField source="reviewer.email"/>
                <TextField source="comment"/>
                <TextField source="question.teacher.full_name"/>
                <TextField source="question.question_image"/>
                <TextField source="question.course"/>
                <TextField source="question.subject"/>
                <TextField source="question.comment"/>
                <TextField source="quality_rate"/>
                <TextField source="difficulty_rate"/>
                <BooleanField source="is_proper"/>
                <DateField source="created_at"/>
                <EditButton basePath="/feedbacks"/>
                <DeleteButton basePath="/feedbacks"/>
            </Datagrid>
        </List>
    );


    export const FeedbackEdit = (props) => (
        <Edit {...props}>
            <SimpleForm>
                <DisabledInput source="id"/>
                <DisabledInput source="reviewer.full_name"/>
                <DisabledInput source="question.question_image"/>
                <DisabledInput source="created_at"/>
                <TextInput source="reviewer.email"/>
                <TextInput source="comment"/>
                <TextInput source="quality_rate"/>
                <TextInput source="difficulty_rate"/>
                <DisabledInput source="question.teacher.full_name"/>
                <DisabledInput source="question.comment"/>
                <BooleanInput source="is_proper"/>
            </SimpleForm>
        </Edit>
    );

    export const FeedbackCreate = (props) => (
        <Create title="Create a Feedback" {...props}>
            <SimpleForm>
                <TextInput source="question.id"/>
                <TextInput source="reviewer.email"/>
                <TextInput source="comment"/>
                <TextInput source="quality_rate"/>
                <TextInput source="difficulty_rate"/>
                <BooleanInput source="is_proper"/>
            </SimpleForm>
        </Create>
    );
    //app.js
      <Resource name="feedbacks" list={FeedbackList} edit={FeedbackEdit} create={FeedbackCreate} />


The code field given above describes user components. FeedbackList, FeedbackEdit and
FeedbackCreate has necessary forms and fields. This views passed into Admin component in *App.js*.