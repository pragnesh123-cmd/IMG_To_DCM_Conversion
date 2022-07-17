custom_tags_dict ={ 
        0x20131000: ('LO', '1', 'ConversionSoftware'),  
        0x20131001: ('LO', '1', 'ConversionSoftwareVersion'),  
        0x20131002: ('LO', '1', 'ReconMatrixPE'),  
        0x20131003: ('LO', '1', 'AnonymisedSerialNumber'),
        0x20131004: ('LO', '1', 'AnonymisedMRICentre'), 
        0x20131005: ('LO', '1', 'PhaseEncodingAxis'),  
        0x20131006: ('LO', '1', 'ShimSetting'), 
        0x20131007: ('LO', '1', 'TxRefAmp'),  
        0x20131008: ('LO', '1', 'AnonymisedStationName'), 
        0x20131009: ('LO', '1', 'DwellTime'),  
        0x2013100A: ('LO', '1', 'ConsistencyInfo'),
        0x2013100B: ('LO', '1', 'ReceiveCoilActiveElements'), 
        0x2013100C: ('LO', '1', 'Interpolation2D'),  
        0x2013100D: ('LO', '1', 'VendorReportedEchoSpacing'),  
        0x2013100E: ('LO', '1', 'RawImage'),  
        0x2013100F: ('LO', '1', 'PhaseOversampling'),  
        0x20131010: ('LO', '1', 'StudyName'), 
        0x20131011: ('LO', '1', 'AnatomicalArea'),  
        0x20131012: ('LO', '1', 'DiseaseArea'),  
        0x20131013: ('LO', '1', 'AnnotationAvailability'),  
        0x20131014: ('LO', '1', 'AnnotationFileName'), 
        0x20131015: ('LO', '1', 'TypeofLabels'),
        0x20131016: ('LO', '1', 'PhilipsRescaleIntercept'),  
        0x20131017: ('LO', '1', 'PhilipsRescaleSlope'), 
        0x20131018: ('LO', '1', 'PhilipsRWVIntercept'),  
        0x20131019: ('LO', '1', 'PhilipsRWVSlope'),  
        0x2013101A: ('LO', '1', 'PhaseEncodingDirection'),  
        0x2013101B: ('LO', '1', 'PhilipsScaleSlope'),  
        0x2013101C: ('LO', '1', 'UsePhilipsFloatNotDisplayScaling') 
    }
        
commands_to_run = {
            'ConversionSoftware' : "block.add_new(0x00,'LO','value')",
            'ConversionSoftwareVersion' :"block.add_new(0x01,'LO','value')",
            'ReconMatrixPE' : "block.add_new(0x02,'LO','value')",
            'AnonymisedSerialNumber':"block.add_new(0x03,'LO','value')",
            'AnonymisedMRICentre':"block.add_new(0x04,'LO','value')",
            'PhaseEncodingAxis':"block.add_new(0x05,'LO','value')", 
            'ShimSetting':"block.add_new(0x06,'LO','value')",  
            'TxRefAmp':"block.add_new(0x07,'LO','value')",  
            'AnonymisedStationName':"block.add_new(0x08,'LO','value')",  
            'DwellTime':"block.add_new(0x09,'LO','value')",  
            'ConsistencyInfo' :"block.add_new(0x0A,'LO','value')",
            'ReceiveCoilActiveElements' :"block.add_new(0x0B,'LO','value')", 
            'Interpolation2D':"block.add_new(0x0C,'LO','value')", 
            'VendorReportedEchoSpacing':"block.add_new(0x0D,'LO','value')",  
            'RawImage':"block.add_new(0x0E,'LO','value')", 
            'PhaseOversampling':"block.add_new(0x0F,'LO','value')",  
            'StudyName':"block.add_new(0x10,'LO','value')", 
            'AnatomicalArea' :"block.add_new(0x11,'LO','value')",   
            'DiseaseArea':"block.add_new(0x12,'LO','value')",
            'AnnotationAvailability':"block.add_new(0x13,'LO','value')",  
            'AnnotationFileName':"block.add_new(0x14,'LO','value')",  
            'TypeofLabels':"block.add_new(0x15,'LO','value')",
            'PhilipsRescaleIntercept':"block.add_new(0x16,'LO','value')",
            'PhilipsRescaleSlope' :"block.add_new(0x17,'LO','value')", 
            'PhilipsRWVIntercept' : "block.add_new(0x18,'LO','value')",  
            'PhilipsRWVSlope' :"block.add_new(0x19,'LO','value')", 
            'PhaseEncodingDirection' : "block.add_new(0x1A,'LO','value')",  
            'PhilipsScaleSlope':"block.add_new(0x1B,'LO','value')",  
            'UsePhilipsFloatNotDisplayScaling':"block.add_new(0x1C,'LO','value')" 
            }

mandatory_tags = ["block.add_new(0x10,'LO','NS study')",
                  "block.add_new(0x11,'LO','Brain')",  
                  "block.add_new(0x12,'LO','MS')",
                  "block.add_new(0x13,'LO','')",
                  "block.add_new(0x14,'LO','')", 
                  "block.add_new(0x15,'LO','')"]
       