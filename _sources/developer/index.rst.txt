Developer Guide
===============

Back-End
----

Server side of the Question Collector is built on a **RESTful API** created with Flask RESTful.
Most of the API endpoints satisfy REST standards. API is authenticated with token based
authentication.

   .. code-block:: python

      #server.py

      app = Flask(__name__)
      cors = CORS(app, resources={r"/*": {"origins": "*"}})
      api = Api(app)

      if __name__ == "__main__":
      app.run(debug=True  )


The code given below the parth of the project that runs Flask and API. In this part **CORS
(Cross-Origin Resource Sharing)** should be set to receive requests from clients. This API is open for
all requests coming from all defined port addresses.

.. toctree::

   database
   models
   views


Front-End
---------

Client side of the project is built on `React.js`_ and `react-admin`_.

.. _react-admin: https://marmelab.com/react-admin/index.html
.. _React.js: https://reactjs.org/


   .. code-block:: javascript

    //app.js
     const App = () => (
	<Admin dashboard={Dashboard}
		   dataProvider={dataProvider}
		   authProvider={authProvider}
		   title="Question Collector"
	>
		<Resource name="users" list={UserList} edit={UserEdit} create={UserCreate} />
		<Resource name="questions" list={QuestionList} edit={QuestionEdit} create={QuestionCreate} />
		<Resource name="feedbacks" list={FeedbackList} edit={FeedbackEdit} create={FeedbackCreate} />
	</Admin>
    );

    export default App


In the code block given above describes underlying structure of the front end app. Admin component
is the main component of *react-admin.*  It takes some propes like dashboard and providers.

**Data Provider**

 .. code-block:: javascript

    //dataProvider.js
    case GET_LIST: {
			return {
				url: `${API_URL}/${resource}`,
				options: {
					headers: headers
				}
			};
		}

    export default App

This project has different *GET_LIST* method type than standard *react-admin* because of the
lack of the server side's paramater handling.

**Auth Provider**

 .. code-block:: javascript

    //authProvider.js
    	if (type === AUTH_LOGIN) {
		const { username, password } = params;
		const request = new Request('${API_URL}/auth', {
			method: 'POST',
			body: JSON.stringify({ username, password }),
			headers: new Headers({ 'Content-Type': 'application/json' }),
		})
		return fetch(request)
			.then(response => {
				if (response.status < 200 || response.status >= 300) {
					throw new Error(response.statusText);
				}
				return response.json();
			})
			.then(({ token }) => {
				localStorage.setItem('token', token);
				localStorage.setItem('user', username);
			});
	}

Auth provider makes a post request to *${API_URL}/auth* with username and password params. If
requests returns with success code, it stores the token in local browser memory. After that, in code
block given below, token is added every request from client.

.. code-block:: javascript

    //dataprovider.js
    let headers = new Headers({Accept: 'application/json'});
	const token = localStorage.getItem('token');
	headers.set('Authorization', `Bearer ${token}`);



.. toctree::

   dashboard
   users
   questions
   feedbacks
