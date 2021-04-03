USE [lego_outbound]
GO

INSERT INTO [dbo].[DivertConfirmationMessages]
           ([Content]
           ,[IsAck]
           ,[correlationId]
           ,[Type]
           ,[created_at]
           ,[updated_at])
     VALUES
           ('   {
            "sequenceNumber": "00001",
            "timeStamp": "2020-10-06T10:42:55",
            "messageName": "DVTCF",
            "correlationId": "20989c0a-7340-4fcb-a2ec-1564f64ed3fa",
            "message": {
                "reasonCode":"",
                "LaneActual":"L2",
                "status": "S",
                "lpId": "090000078760455",
                "orderId": "121294578",
                "shipId": "1",
                "wave": "2525166",
                "taskId": "287159079",
                "weight": "2.25",
                "width": "14",
                "length": "12",
                "height": "7.25",
                "containerType": "LG2",
                "carrier": "FEDX",
                "trackingNumber": "",
                "manifestId": "",
                "route": "",
                "sscc": "00000000000379916117",
                "accountNumber": "",
                "shipToPostalCode": "80013",
                "shipToState": "CO",
                "shipToCountry": "US",
                "shipDate": ""
            }
        }'
           ,0
           ,'20989c0a-7340-4fcb-a2ec-1564f64ed3fb'
           ,'DVTCF'
           ,GETDATE()
           ,GETDATE())
GO

INSERT INTO [dbo].[DivertConfirmationMessages]
           ([Content]
           ,[IsAck]
           ,[correlationId]
           ,[Type]
           ,[created_at]
           ,[updated_at])
     VALUES
           ('   {
            "sequenceNumber": "00002",
            "timeStamp": "2020-10-06T10:42:55",
            "messageName": "DVTCF",
            "correlationId": "20989c0a-7340-4fcb-a2ec-1564f64ed3fb",
            "message": {
                "reasonCode":"",
                "LaneActual":"L2",
                "status": "S",
                "lpId": "090000078760456",
                "orderId": "121294578",
                "shipId": "1",
                "wave": "2525166",
                "taskId": "287159079",
                "weight": "2.25",
                "width": "14",
                "length": "12",
                "height": "7.25",
                "containerType": "LG2",
                "carrier": "FEDX",
                "trackingNumber": "",
                "manifestId": "",
                "route": "",
                "sscc": "00000000000379916118",
                "accountNumber": "",
                "shipToPostalCode": "80013",
                "shipToState": "CO",
                "shipToCountry": "US",
                "shipDate": ""
            }
        }'
           ,0
           ,'20989c0a-7340-4fcb-a2ec-1564f64ed3fc'
           ,'DVTCF'
           ,GETDATE()
           ,GETDATE())
GO


INSERT INTO [dbo].[DivertConfirmationMessages]
           ([Content]
           ,[IsAck]
           ,[correlationId]
           ,[Type]
           ,[created_at]
           ,[updated_at])
     VALUES
           ('   {
            "sequenceNumber": "00003",
            "timeStamp": "2020-10-06T10:42:55",
            "messageName": "DVTCF",
            "correlationId": "20989c0a-7340-4fcb-a2ec-1564f64ed3fc",
            "message": {
                "reasonCode":"",
                "LaneActual":"L2",
                "status": "S",
                "lpId": "090000078760457",
                "orderId": "121294578",
                "shipId": "1",
                "wave": "2525166",
                "taskId": "287159079",
                "weight": "2.25",
                "width": "14",
                "length": "12",
                "height": "7.25",
                "containerType": "LG2",
                "carrier": "FEDX",
                "trackingNumber": "",
                "manifestId": "",
                "route": "",
                "sscc": "00000000000379916119",
                "accountNumber": "",
                "shipToPostalCode": "80013",
                "shipToState": "CO",
                "shipToCountry": "US",
                "shipDate": ""
            }
        }'
           ,0
           ,'20989c0a-7340-4fcb-a2ec-1564f64ed3fc'
           ,'DVTCF'
           ,GETDATE()
           ,GETDATE())
GO




INSERT INTO [dbo].[DivertConfirmationMessages]
           ([Content]
           ,[IsAck]
           ,[correlationId]
           ,[Type]
           ,[created_at]
           ,[updated_at])
     VALUES
           ('   {
            "sequenceNumber": "00004",
            "timeStamp": "2020-10-06T10:42:55",
            "messageName": "DVTCF",
            "correlationId": "20989c0a-7340-4fcb-a2ec-1564f64ed3fd",
            "message": {
                "reasonCode":"",
                "LaneActual":"L2",
                "status": "S",
                "lpId": "090000078760458",
                "orderId": "121294578",
                "shipId": "1",
                "wave": "2525166",
                "taskId": "287159079",
                "weight": "2.25",
                "width": "14",
                "length": "12",
                "height": "7.25",
                "containerType": "LG2",
                "carrier": "FEDX",
                "trackingNumber": "",
                "manifestId": "",
                "route": "",
                "sscc": "00000000000379916120",
                "accountNumber": "",
                "shipToPostalCode": "80013",
                "shipToState": "CO",
                "shipToCountry": "US",
                "shipDate": ""
            }
        }'
           ,0
           ,'0989c0a-7340-4fcb-a2ec-1564f64ed3fc'
           ,'DVTCF'
           ,GETDATE()
           ,GETDATE())
GO

