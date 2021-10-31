# uidai-address-formatting
Aadhar UIDAI Address Formatting Code

Hello, this is team Revolutionary coders, we are presenting you our address formatting solution

address_formatting_app.py is the api that needs to be implemented to the code

we have created another file that can help you with the testing purposes post_request.py takes input from our dummy data file
Address_data.json and returns a formatted json file which is the desired output. post_request.py then saves it in a csv format
for easy reading.
You can use your code to post a json request and it will return a json file any further tweaks in the post_request python file
are done for the purpose of debugging and presentation of this video.


Why is our code a good implementation..?

Accuracy of output
-> Grouping of repetitive components : our code easily handles repitition and judges which strings to cast out.
-> Final Address presentation : oriented in json 'records' format, very user friendly.
-> Accuracy: Unlike ML and Deep Learning models, we have explicitly coded because training an AI model in 4 days is not a reliable coding practice. It may be catastrophic in its' accuracy. With explicit coding, our hardwork pays off to a sufficiently good accuracy.

Optimization Strength
->Handling of Urban and rural addresses: unlike ML models which may fail in such cases, our model is not affected by rural addresses
->Handling of edge/boundary cases:
	a)Non availibility of repetitive componenets: Any repititions even if they were a substring of a larger overall string, are removed
	b)Extreme repititive scenarios: multiple repitition does not impair our code's judement about which data is to be removedand which should be retained
	c)Non availibility of Some Address Compnents: Null values does not interfere with our api
	d)Availability of special charecters: Any special characters do not interfere with our coding
	e)Non traditional spelling error handling: we have implemented a non traditional approach that can deal with 1-2 missed alphabetsper string

Handling of local language address: We aare using indic_transliteration to handle local languages

API Design: We have designed a simple and lightweight flask api and executed a simple implementation. It is a standard api which expects a json input and throws a json ouptut. It uses POST argument keeping the contents of the jsonn file safe
Performance at scale: This api implementation will work well at a larger scale of data since it implements pandas dataframe which are is most popular choice for many big data implementation purposes

Execution of code: After this video, you would find it easy to execute our code

Code quality:
	a)Organization and readability: It is a small code of 300 lines, well organised and indented, easy to read with good commenting
	b)security Consideration: The best security consideration is POSTing the requests instead of using GET. Since this is a locally usable api, security threats are otherwise very low

