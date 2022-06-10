function [errorCode, EventTriggerConfiguration, ActionConfiguration] = EventExtendedGet(socketId, ID)
%EventExtendedGet :  Read the event and action configuration defined by ID
%
%	[errorCode, EventTriggerConfiguration, ActionConfiguration] = EventExtendedGet(socketId, ID)
%
%	* Input parameters :
%		int32 socketId
%		int32 ID
%	* Output parameters :
%		int32 errorCode
%		cstring EventTriggerConfiguration
%		cstring ActionConfiguration


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
EventTriggerConfiguration = '';
for i = 1:205
	EventTriggerConfiguration = [EventTriggerConfiguration '          '];
end
ActionConfiguration = '';
for i = 1:205
	ActionConfiguration = [ActionConfiguration '          '];
end

% lib call
[errorCode, EventTriggerConfiguration, ActionConfiguration] = calllib('XPS_Q8_drivers', 'EventExtendedGet', socketId, ID, EventTriggerConfiguration, ActionConfiguration);
