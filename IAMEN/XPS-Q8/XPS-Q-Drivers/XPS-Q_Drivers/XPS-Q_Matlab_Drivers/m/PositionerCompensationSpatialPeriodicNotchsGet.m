function [errorCode, SpatialNotchStep1, SpatialNotchBandwidth1, SpatialNotchGain1, SpatialNotchStep2, SpatialNotchBandwidth2, SpatialNotchGain2, SpatialNotchStep3, SpatialNotchBandwidth3, SpatialNotchGain3] = PositionerCompensationSpatialPeriodicNotchsGet(socketId, PositionerName)
%PositionerCompensationSpatialPeriodicNotchsGet :  Read spatial compensation notch filters parameters 
%
%	[errorCode, SpatialNotchStep1, SpatialNotchBandwidth1, SpatialNotchGain1, SpatialNotchStep2, SpatialNotchBandwidth2, SpatialNotchGain2, SpatialNotchStep3, SpatialNotchBandwidth3, SpatialNotchGain3] = PositionerCompensationSpatialPeriodicNotchsGet(socketId, PositionerName)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%	* Output parameters :
%		int32 errorCode
%		doublePtr SpatialNotchStep1
%		doublePtr SpatialNotchBandwidth1
%		doublePtr SpatialNotchGain1
%		doublePtr SpatialNotchStep2
%		doublePtr SpatialNotchBandwidth2
%		doublePtr SpatialNotchGain2
%		doublePtr SpatialNotchStep3
%		doublePtr SpatialNotchBandwidth3
%		doublePtr SpatialNotchGain3


% Test that library is loaded
if (~libisloaded('XPS_C8_drivers'))
	disp 'Please load XPS_C8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
SpatialNotchStep1 = 0;
SpatialNotchBandwidth1 = 0;
SpatialNotchGain1 = 0;
SpatialNotchStep2 = 0;
SpatialNotchBandwidth2 = 0;
SpatialNotchGain2 = 0;
SpatialNotchStep3 = 0;
SpatialNotchBandwidth3 = 0;
SpatialNotchGain3 = 0;

% lib call
[errorCode, PositionerName, SpatialNotchStep1, SpatialNotchBandwidth1, SpatialNotchGain1, SpatialNotchStep2, SpatialNotchBandwidth2, SpatialNotchGain2, SpatialNotchStep3, SpatialNotchBandwidth3, SpatialNotchGain3] = calllib('XPS_C8_drivers', 'PositionerCompensationSpatialPeriodicNotchsGet', socketId, PositionerName, SpatialNotchStep1, SpatialNotchBandwidth1, SpatialNotchGain1, SpatialNotchStep2, SpatialNotchBandwidth2, SpatialNotchGain2, SpatialNotchStep3, SpatialNotchBandwidth3, SpatialNotchGain3);
