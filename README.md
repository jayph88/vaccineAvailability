# vaccineAvailability
this project helps to identify vaccination availability near you based on age and pin codes


### commandline execution:  
```
# install requirements
pip install -r requirements.txt

# print usage
python commandline_exec.py -h

# example   
python commandline_exec.py --age 20 --pin "411057,411001,411033,411011,411006"
```

### aws lambda:
1. build externals
```
# docker command to create python directory from externals
docker run --rm --volume=<dir of project>:/lambda-build -w=/lambda-build lambci/lambda:build-python3.7 pip install -r requirements.txt --target python

# example
docker run --rm --volume=D:\gitlab\vaccineAvailability:/lambda-build -w=/lambda-build lambci/lambda:build-python3.7 pip install -r requirements.txt --target python
```

2. zip "python" directory by above command and upload it as lambda layer for lambda function

3. create event in aws to trigger lambda, here you can configure how frequent you want to invoke lambda
[trigger for lambda](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-run-lambda-schedule.html)

####note:
You will need to change SNS_ARN in email_notification.py with your own 



   
    
  
