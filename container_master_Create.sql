USE [lego_outbound]
GO

/****** Object:  Table [dbo].[container_master]    Script Date: 10/27/2020 1:22:16 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[container_master](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[LPID] [nvarchar](15) NULL,
	[CorrelationId] [nvarchar](500) NULL,
	[Status] [nvarchar](1)  NULL,
	[OrderId] [int]  NULL,
	[ShipId] [int] NULL,
	[Wave] [int] NULL,
	[TaskId] [int] NULL,
	[Weight] [decimal](5, 2) NULL,
	[Width] [decimal](5, 2) NULL,
	[Length] [decimal](5, 2) NULL,
	[Height] [decimal](5, 2) NULL,
	[ContainerType] [nvarchar](30) NULL,
	[Carrier] [nvarchar](4)  NULL,
	[TrackingNumber] [nvarchar](30) NULL,
	[SSCC] [nchar](20) NULL,
	[AccountNumber] [nvarchar](255) NULL,
	[ZipCode] [nvarchar](12) NULL,
	[State] [nchar](2) NULL,
	[Country] [nchar](3) NULL,
	[ShipDate] [datetime] NULL,
	[ASNHDRPASSTHRUCHAR19] [nvarchar](255) NULL,
	[LaneAssign] [int] NULL,
	[LaneActual] [int] NULL,
	[ReasonCode] [int] NULL,
	[ReasonDescription] [nvarchar](30) NULL,
	[IsAck] [bit] NOT NULL,
	[VerifyProcessed] [bit] NOT NULL,
	[CreatedAt] [datetime] NOT NULL,
	[UpdatedAt] [datetime] NOT NULL
) ON [PRIMARY]
GO


