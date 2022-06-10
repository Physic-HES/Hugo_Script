function [errorCode] = PositionerCompensationSpatialPeriodicNotchsSet(socketId, PositionerName, SpatialNotchStep1, SpatialNotchBandwidth1, SpatialNotchGain1, SpatialNotchStep2, SpatialNotchBandwidth2, SpatialNotchGain2, SpatialNotchStep3, SpatialNotchBandwidth3, SpatialNotchGain3)
%PositionerCompensationSpatialPeriodicNotchsSet :  Update spatial compensation notch filters parameters 
%
%	[errorCode] = PositionerCompensationSpatialPeriodicNotchsSet(socketId, PositionerName, SpatialNotchStep1, SpatialNotchBandwidth1, SpatialNotchGain1, SpatialNotchStep2, SpatialNotchBandwidth2, SpatialNotchGain2, SpatialNotchStep3, SpatialNotchBandwidth3, SpatialNotchGain3)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%		double SpatialNotchStep1
%		double SpatialNotchBandwidth1
%		double SpatialNotchGain1
%		double SpatialNotchStep2
%		double SpatialNotchBandwidth2
%		double SpatialNotchGain2
%		double SpatialNotchStep3
%		double SpatialNotchBandwidth3
%		double SpatialNotchGain3
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_C8_drivers'))
	disp 'Please load XPS_C8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode, PositionerName] = calllib('XPS_C8_drivers', 'PositionerCompensationSpatialPeriodicNotchsSet', socketId, PositionerName, SpatialNotchStep1, SpatialNotchBandwidth1, SpatialNotchGain1, SpatialNotchStep2, SpatialNotchBandwidth2, SpatialNotchGain2, SpatialNotchStep3, SpatialNotchBandwidth3, SpatialNotchGain3);
