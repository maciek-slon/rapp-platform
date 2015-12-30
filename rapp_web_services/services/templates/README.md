RAPP Platform Web Services Development Templates
-------------------------------------

## Synopsis

Use these templates/examples as the ground-truth to develop and/or extend RAPP Platform Web Services (a.k.a HOP Web Services).

While developing RAPP Platform Web Services, you might want to read on [HOP/hopjs](https://github.com/manuel-serrano/hop)

If you are not familiar with server-side applications, you might also have to read on [Nodejs](https://nodejs.org/en/)


## Templates

To make development of HOP Web Services more attractive and understandable, we provide two template source files:

- web_service.template.js
- web_service_post_file.template.js

Using these templates as a reference while developing HOP Web Services, might save you alot of hours studying!
In most cases, you might have to change just a few lines of code!

#### web_service.template.js

Illustrates a web-service implementation with, multiple input arguments, ROS interface, asynchronous response.


#### web_service_post_file.template.js

Illustrates a web-service implementation with, multiple input arguments, file transfers, ROS interface, asynchronous response.


##Notable comment:

Currently a bug on HOP http request parser exists, which let all service input parameters to be parsed as strings.
For example:

```javascript
service foo( {str: '', num: 0} ){
	console.log(typeof str);
	console.log(typeof num);
}
```

will report both **str** and num arguments to be of type **String**.

To overcome this issue in case of **Number** or **Boolean** data types, you have to manually cast to the appropriate type

```javascript
service foo( {bool_arg: false, num_arg: 0} ){
  	//  Dynamic cast to Boolean.
	if (bool_arg === 'True' || bool_arg === 'true') {bool_arg = true;}
  	else {bool_arg = false;}

	// Dynamic cast to Number.
	num_arg = parseInt(num_arg);
}
```

## Contributors

- Konstaninos Panayiotou, [klpanagi@gmail.com]
- Manos Tsardoulias, [etsardou@gmail.com]
